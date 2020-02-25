from collections import OrderedDict
import json
from pathlib import Path

from pynando.data import find


class NandoNode(object):
    def __init__(
            self, _id, name_ja, synonyms_ja, name_en, synonyms_en,
            is_defined_by, see_also, is_parent, class_id, notification_no,
            _parents_ids=None, _children_ids=None,
            mondo_nodes=None, mondo_node_candidates=None
    ):
        self.id = _id
        self.name_ja = name_ja
        self.synonyms_ja = synonyms_ja
        self.name_en = name_en
        self.synonyms_en = synonyms_en
        self.is_defined_by = is_defined_by
        self.see_also = see_also
        self.is_parent = is_parent
        self.class_id = class_id
        self.notification_no = notification_no

        if _parents_ids is None:
            self._parents_ids = []
        else:
            self._parents_ids = _parents_ids
        if _children_ids is None:
            self._children_ids = []
        else:
            self._children_ids = _children_ids

        self.parents = set()
        self.children = set()

        if mondo_nodes is None:
            self.mondo_nodes = []
        else:
            self.mondo_nodes = mondo_nodes
        if mondo_node_candidates is None:
            self.mondo_node_candidates = []
        else:
            self.mondo_node_candidates = mondo_node_candidates

    def __repr__(self):
        lines = [
            'id: {}'.format(self.id),
            'name_ja: {}'.format(self.name_ja),
            'synonyms_ja: {}'.format(' | '.join(self.synonyms_ja)),
            'name_en: {}'.format(self.name_en),
            'synonyms_en: {}'.format(' | '.join(self.synonyms_en)),
            'children: {}'.format(', '.join(sorted([c.id for c in self.children]))),
        ]
        return '\n'.join(lines)

    def link(self, nando_node_dict):
        for parent_id in self._parents_ids:
            parent_nando_node = nando_node_dict[parent_id]
            self.parents.add(parent_nando_node)
            parent_nando_node.children.add(self)

    def to_json(self):
        return {
            'id': self.id,
            'name_ja': self.name_ja,
            'synonyms_ja': self.synonyms_ja,
            'name_en': self.name_en,
            'synonyms_en': self.synonyms_en,
            'mondo_nodes': [m.to_json() for m in self.mondo_nodes],
            'mondo_node_candidates': [m.to_json() for m in self.mondo_node_candidates],
            'is_defined_by': self.is_defined_by,
            'see_also': self.see_also,
            'children': sorted([c.id for c in self.children]),
            'class_id': self.class_id,
            'notification_no': self.notification_no,
        }


class Nando(object):
    def __init__(self, resource_name: str):
        self.root = NandoNode(
            _id='0',
            name_ja='root',
            synonyms_ja=[],
            name_en='root',
            synonyms_en=[],
            is_defined_by=None,
            see_also=[],
            is_parent=True,
            class_id=None,
            notification_no=None,
        )
        self.nando_node_dict = {'0': self.root}
        self.fp = find(resource_name)
        self.read(self.fp)

    def __len__(self):
        return len(self.nando_node_dict)

    def __iter__(self):
        return iter(OrderedDict(self.nando_node_dict).values())

    def __getitem__(self, item):
        return self.nando_node_dict[item]

    def read(self, fp: Path):
        """read the json file"""
        with fp.open() as f:
            for nando_data in json.load(f):
                _id = nando_data['id']
                if _id == '0':
                    is_parent = True
                    _parents_ids = []
                elif '-' not in _id:
                    is_parent = True
                    _parents_ids = ['0']
                else:
                    is_parent = False
                    _parents_ids = [_id.rsplit('-', 1)[0]]

                nando_node = NandoNode(
                    _id=_id,
                    name_ja=nando_data['name_ja'],
                    synonyms_ja=nando_data['synonyms_ja'],
                    name_en=nando_data['name_en'],
                    synonyms_en=nando_data['synonyms_en'],
                    is_defined_by=nando_data['is_defined_by'],
                    see_also=nando_data['see_also'],
                    is_parent=is_parent,
                    class_id=nando_data['class_id'],
                    notification_no=nando_data['notification_no'],
                    _parents_ids=_parents_ids,
                    _children_ids=nando_data.get('children', []),
                )
                self.nando_node_dict[_id] = nando_node

        nando_nodes = set(self.nando_node_dict.values())
        for nando_node in nando_nodes:
            nando_node.link(self.nando_node_dict)

    def save(self, fp: Path):
        """save to a json file"""
        with fp.open(mode='w') as f:
            nando_node_list = [n.to_json() for n in self]
            json.dump(nando_node_list, f, indent=4, ensure_ascii=False)

    # def evaluate(self, target):
    #     """
    #     MONDOとの紐付き状況を評価
    #     さらに紐付いていないnando_nodeをtargetに応じて集計
    #         - en_names: 英語名の有無
    #         - candidates: 候補MONDOの有無
    #         - hierarchy: 親子関係ごとのマッチ状況
    #     :param target: ['en_names', 'candidates']
    #     :return:
    #     """
    #     total = len(self) - 1  # rootを除く
    #     nando_wo_mondos = [n for n in self if not (n.mondo_nodes or n.id == '0')]
    #     wo_mondos_num = len(nando_wo_mondos)
    #     lines = '総数: 100% ({} entities)\n'.format(total)
    #     lines += '    ├ マッチあり: {:.1%}  ({} entities)\n'.format(1 - wo_mondos_num / total, total - wo_mondos_num)
    #     lines += '    └ マッチなし: {:.1%}  ({} entities)\n'.format(wo_mondos_num / total, wo_mondos_num)
    #
    #     if target == 'en_names':
    #         no_en_num = sum([1 for n in nando_wo_mondos if not (n.name_en or n.synonyms_en)])
    #         w_en_ratio, wo_en_ratio = (wo_mondos_num - no_en_num) / total, no_en_num / total
    #         lines += '        ├ 英語疾患名あり: {:.1%}  ({} entities)\n'.format(w_en_ratio, wo_mondos_num - no_en_num)
    #         lines += '        └ 英語疾患名なし: {:.1%}  ({} entities)\n'.format(wo_en_ratio, no_en_num)
    #     elif target == 'candidates':
    #         wo_candidates_num = sum([1 for n in nando_wo_mondos if not (n.mondo_nodes or n.mondo_node_candidates)])
    #         w_candidates_ratio, wo_candodates_ratio = (wo_mondos_num - wo_candidates_num) / total, wo_candidates_num / total
    #         lines += '        ├ 候補MONDOあり: {:.1%}  ({} entities)\n'.format(w_candidates_ratio, wo_mondos_num - wo_candidates_num)
    #         lines += '        └ 候補MONDOなし: {:.1%}  ({} entities)\n'.format(wo_candodates_ratio, wo_candidates_num)
    #     elif target == 'hierarchy':
    #         nando_wo_mondos_parent = [n for n in nando_wo_mondos if n.is_parent]
    #         parent_num = len(nando_wo_mondos_parent)
    #         parent_ratio = parent_num / total
    #         parent_w_matched_child_num = sum([
    #             1 for n in nando_wo_mondos_parent
    #             if any(c.mondo_nodes for c in n.children)
    #         ])
    #         parent_w_matched_child_ratio = parent_w_matched_child_num / total
    #         parent_wo_matched_child_num = parent_num - parent_w_matched_child_num
    #         parent_wo_matched_child_ratio = parent_wo_matched_child_num / total
    #         lines += '        ├ 親: {:.1%}  ({} entities)\n'.format(parent_ratio, parent_num)
    #         lines += '        │   ├ 1つ以上の子でマッチあり: {:.1%}  ({} entities)\n'.format(parent_w_matched_child_ratio, parent_w_matched_child_num)
    #         lines += '        │   └ 全ての子でマッチなし or 子なし: {:.1%}  ({} entities)\n'.format(parent_wo_matched_child_ratio, parent_wo_matched_child_num)
    #
    #         nando_wo_mondos_child = [n for n in nando_wo_mondos if not n.is_parent]
    #         child_num = len(nando_wo_mondos_child)
    #         child_ratio = child_num / total
    #         child_w_matched_parent_num = sum([
    #             1 for n in nando_wo_mondos_child
    #             if any([p.mondo_nodes for p in n.parents])
    #         ])
    #         child_w_matched_parent_ratio = child_w_matched_parent_num / total
    #         child_wo_matched_parent_num = child_num - child_w_matched_parent_num
    #         child_wo_matched_parent_ratio = child_wo_matched_parent_num / total
    #         lines += '        └ 子: {:.1%}  ({} entities)\n'.format(child_ratio, child_num)
    #         lines += '            ├ 親でマッチあり: {:.1%}  ({} entities)\n'.format(child_w_matched_parent_ratio, child_w_matched_parent_num)
    #         lines += '            └ 親でマッチなし: {:.1%}  ({} entities)\n'.format(child_wo_matched_parent_ratio, child_wo_matched_parent_num)
    #
    #     lines += '=' * 100
    #     print(lines)

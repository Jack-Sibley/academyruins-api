import difflib
import re
from abc import ABC, abstractmethod
from typing import Union


class ItemDiffer(ABC):
    DIFF_START_MARKER = "<<<<"
    DIFF_END_MARKER = ">>>>"

    def _wrap_change(self, rule_slice: list[str]) -> (list[str], bool):
        if not rule_slice:
            return [], False
        rule_slice[0] = self.DIFF_START_MARKER + rule_slice[0]
        rule_slice[-1] += self.DIFF_END_MARKER
        return rule_slice, True

    @abstractmethod
    def diff_items(self, old_item, new_item) -> Union[None, tuple]:
        pass


class CRItemDiffer(ItemDiffer):
    def _format_item(self, number: str, text: str) -> dict:
        return {"ruleNum": number, "ruleText": text}

    def wrap_change(self, rule_slice: list[str]) -> (list[str], bool):
        # matches a mention of a rule number / range of numbers
        # TODO actually inspect how this regex works
        rule_mention_regex = r"^(?:rules? )?\d{3}(?:\.\d+[a-z]*)*(?:–\d{3}(?:\.\d+[a-z]?)?)?\)?\.?"
        if re.match(rule_mention_regex, " ".join(rule_slice)):
            # don't mark a change if only rules numbers were modified
            return rule_slice, False
        return ItemDiffer._wrap_change(self, rule_slice)

    def diff_items(self, old_item, new_item) -> Union[None, tuple]:
        old_rule_num = old_item and old_item["ruleNumber"]
        new_rule_num = new_item and new_item["ruleNumber"]
        old_rule_text = old_item and old_item["ruleText"].strip()
        new_rule_text = new_item and new_item["ruleText"].strip()

        if not old_item:
            return None, self._format_item(new_rule_num, new_rule_text)
        if not new_item:
            return self._format_item(old_rule_num, old_rule_text), None

        if old_rule_text == new_rule_text:
            return None

        # we want to diff on whole words, not individual characters
        old_text = old_rule_text.split(" ")
        new_text = new_rule_text.split(" ")

        seq = difflib.SequenceMatcher(None, old_text, new_text)
        matches = seq.get_matching_blocks()

        diffed_old, diffed_new = [], []
        old_offset, new_offset = 0, 0
        changed = False
        for o, n, l in matches:
            change, was_changed = self.wrap_change(old_text[old_offset:o])
            diffed_old.extend(change)
            changed |= was_changed
            change, was_changed = self.wrap_change(new_text[new_offset:n])
            diffed_new.extend(change)
            changed |= was_changed

            diffed_old.extend(old_text[o : o + l])
            diffed_new.extend(new_text[n : n + l])

            old_offset = o + l
            new_offset = n + l

        if not changed:
            return None

        return (
            self._format_item(old_rule_num, " ".join(diffed_old)),
            self._format_item(new_rule_num, " ".join(diffed_new)),
        )

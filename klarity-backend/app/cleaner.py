import re
import unicodedata
from langchain_core.documents import Document as LC_Document


class Cleaner:
    def __init__(self):
        self.page_text_map = {}

    # --------------------------
    # Extract block metadata + text
    # --------------------------
    def _extract_block(self, blk):
        if isinstance(blk, LC_Document):
            pg = blk.metadata.get("page", -1)
            txt = blk.page_content or ""
            return "text", pg, txt, blk.metadata

        if isinstance(blk, dict):
            return blk.get("type"), blk.get("page", -1), blk.get("content"), blk

        return None, -1, None, {}

    # --------------------------
    # Register text per page
    # --------------------------
    def register_page_text(self, pg, text):
        if pg not in self.page_text_map:
            self.page_text_map[pg] = ""
        self.page_text_map[pg] += " " + (text or "")

    # --------------------------
    # Classify real tables
    # --------------------------
    def is_true_table(self, rows):
        if not rows or not isinstance(rows, list):
            return False

        col_counts = [len(r) for r in rows]
        if max(col_counts) < 2:
            return False

        if sum(c >= 2 for c in col_counts) < 3:
            return False

        return True

    # --------------------------
    # Clean normal text
    # --------------------------
    def clean_normal(self, txt):

        txt = unicodedata.normalize("NFKC", txt)
        txt = re.sub(r"(\w+)-\s*\n(\w+)", r"\1\2", txt)
        txt = txt.replace("\n", " ")
        txt = re.sub(r"\s+", " ", txt)

        return txt.strip()

    # --------------------------
    # Clean table cell rows
    # --------------------------
    def clean_table(self, rows):
        cleaned = []
        for r in rows:
            cleaned.append([unicodedata.normalize("NFKC", str(c)).strip() if c else "" for c in r])
        return cleaned

    # --------------------------
    # Convert table rows to text block
    # --------------------------
    def table_to_text(self, rows):
        lines = [" | ".join(r) for r in rows]
        return "\n".join(lines)

    # --------------------------
    # Table discard logic
    # --------------------------
    def should_discard_table(self, rows, pg):
        single = sum(1 for r in rows if len(r) <= 1)
        if single / len(rows) > 0.6:
            return True

        flat = " ".join(c for r in rows for c in r if c).strip()
        if flat and pg in self.page_text_map:
            if flat[:50] in self.page_text_map[pg]:
                return True

        return False

    # --------------------------
    # MAIN PROCESSOR
    # --------------------------
    def process(self, blocks):
        cleaned_docs = []

        # FIRST: register text for duplication checks
        for blk in blocks:
            blk_type, pg, content, meta = self._extract_block(blk)
            if blk_type == "text":
                self.register_page_text(pg, content)

        # SECOND: clean & rebuild Document objects
        for blk in blocks:
            blk_type, pg, content, metadata = self._extract_block(blk)

            # NORMAL TEXT
            if blk_type == "text":
                cleaned = self.clean_normal(content)
                cleaned_docs.append(
                    LC_Document(
                        page_content=cleaned,
                        metadata=metadata
                    )
                )
                continue

            # TABLE
            if blk_type == "table":
                rows = content or []

                rows = [r for r in rows if any(c for c in r if c)]

                if self.should_discard_table(rows, pg):
                    continue

                if self.is_true_table(rows):
                    rows = self.clean_table(rows)
                    table_text = self.table_to_text(rows)

                    new_meta = metadata.copy()
                    new_meta["type"] = "table_cleaned"

                    cleaned_docs.append(
                        LC_Document(
                            page_content=table_text,
                            metadata=new_meta
                        )
                    )

                else:
                    flat = " ".join(c for r in rows for c in r if c)
                    cleaned = self.clean_normal(flat)

                    cleaned_docs.append(
                        LC_Document(
                            page_content=cleaned,
                            metadata=metadata
                        )
                    )

        return cleaned_docs

"""Sphinx-директива `jsonblock` — JSON-код с прикреплённым моноширинным
заголовком-источником (откуда взят JSON).

Использование в MyST-Markdown::

    ```{jsonblock} Condition_Interaction.Self_Uneasy_Lv2 · MCP modkit_get_row
    {
      "Id": "Self_Uneasy_Lv2"
    }
    ```

Опции:
    :draft:  пометить блок как черновик/предложение (адрес — целевой путь,
             а не источник реальных данных); блок подсвечивается иначе.

Аргумент директивы (вся строка после её имени) — это «проп» с адресом/схемой
получения JSON. Он выводится в том же блоке, что и JSON, моноширинным шрифтом
(стили — в _static/custom.css).
"""

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective


class JsonBlock(SphinxDirective):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {"draft": directives.flag}

    def run(self):
        source = self.arguments[0].strip()
        code = "\n".join(self.content)

        classes = ["json-block"]
        if "draft" in self.options:
            classes.append("is-draft")
        container = nodes.container("", classes=classes)

        header = nodes.paragraph("", "", classes=["json-block-source"])
        header += nodes.Text(source)
        container += header

        literal = nodes.literal_block(code, code)
        literal["language"] = "json"
        self.set_source_info(literal)
        container += literal

        return [container]


def setup(app):
    app.add_directive("jsonblock", JsonBlock)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

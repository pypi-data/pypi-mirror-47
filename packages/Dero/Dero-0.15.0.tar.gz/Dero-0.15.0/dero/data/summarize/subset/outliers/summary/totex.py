from dero.data.summarize.subset.outliers.typing import DfDict
from dero.data.typing import DocumentOrTable
import dero.latex.table as lt
from dero.latex import Document

def df_dict_to_table(df_dict: DfDict, as_document: bool=False,
                     author: str=None, caption: str=None) -> DocumentOrTable:

    table = lt.Table.from_panel_name_df_dict(
        df_dict,
        include_index=True,
        top_left_corner_labels='Variable',
        caption=caption,
        landscape=True
    )

    if as_document:
        return Document(
            table,
            author=author,
            title=caption
        )

    return table
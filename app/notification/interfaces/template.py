from requests import Session

from notification.models.schemas.template import TemplateCreateSchema, TemplateUpdateSchema, TemplateGetMultiSchema
from notification.models.template import template_crud, NtfTemplate
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase


class TemplateInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = crud

    @staticmethod
    def _get_key_words(text: str) -> list:
        keywords = []
        start = text.find("@@")
        while start != -1:
            end = text.find("@@", start + 2)
            if end != -1:
                keywords.append(text[start + 2:end])
            start = text.find("@@", end + 2)
        return keywords

    def _replace_key_words(self, template_text: str, key_value_dict: dict):
        for key, value in key_value_dict.items():
            if key not in self._get_key_words(template_text):
                raise ValueError(f"Keyword '{key}' not found in the text")

            template_text = f"""{template_text}"""
            template_text = template_text.replace("@@" + str(key) + "@@", str(value) if value != None or value != None else '')

        return template_text

    def generate_text_with_template_name(self, db: Session, template_name: str, key_value_dict: dict):
        template_obj: NtfTemplate = self.find_item_multi(db=db, name=template_name)[0]
        generated_text = self._replace_key_words(template_text=template_obj.text, key_value_dict=key_value_dict)
        return generated_text, template_obj.id, template_obj.title


template_agent = TemplateInterface(
    template_crud,
    TemplateCreateSchema,
    TemplateUpdateSchema,
    TemplateGetMultiSchema
)

from sqlalchemy import Column, Integer, String, ForeignKey

from notification.models.schemas.template import TemplateCreateSchema, TemplateUpdateSchema, TemplateGetMultiSchema
from system.base.crud import CRUDBase, ModelType
from system.dbs.models import Base


class NtfTemplate(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    text = Column(String, nullable=False)  # Sign the special words with two "@" after and before the word. @@otp@@
    title = Column(String, nullable=False)


class TemplateCRUD(
    CRUDBase[
        NtfTemplate,
        TemplateCreateSchema,
        TemplateUpdateSchema,
        TemplateGetMultiSchema
    ]
):
    pass


template_crud = TemplateCRUD(NtfTemplate)

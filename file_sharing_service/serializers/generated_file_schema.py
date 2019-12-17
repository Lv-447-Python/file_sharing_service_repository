"""Schema for file_sharing_service"""

from file_sharing_service import MARSHMALLOW
from file_sharing_service.models.generated_file import GeneratedFile


class GeneratedFileSchema(MARSHMALLOW.ModelSchema):
    """
    Schema for GeneratedFile Model
    """
    class Meta:
        """
        Class meta for model schema GeneratedFile
        """
        model = GeneratedFile

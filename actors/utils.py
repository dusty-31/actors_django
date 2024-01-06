class DataMixin:
    """
    This class, DataMixin, is a mixin class that can be used to add additional data to a context dictionary.

    Attributes:
        title_page (str): The title of the page.
        category_selected (str): The selected category.
        extra_content (dict): Additional content to be added to the context dictionary.

    Methods:
        __init__(self)
            Initializes the DataMixin instance.
            If the title_page attribute is not None, it adds its value to the extra_content dictionary with the key
            'title'. If the category_selected attribute is not None, it adds its value to the
            extra_content.
            dictionary with the key 'category_selected'.

        get_mixin_context(self, context: dict, **kwargs) -> dict
            Adds the extra_content and the provided keyword arguments to the given context dictionary and returns the updated context.
    """

    title_page = None
    category_selected = None
    extra_content = {}

    def __init__(self) -> None:
        if self.title_page:
            self.extra_content['title'] = self.title_page

        if self.category_selected is not None:
            self.extra_content['category_selected'] = self.category_selected

    def get_mixin_context(self, context: dict, **kwargs) -> dict:
        context.update(self.extra_content)
        context.update(kwargs)
        return context

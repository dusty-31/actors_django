class DataMixin:
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

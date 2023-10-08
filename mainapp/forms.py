from django import forms
from django.core.exceptions import ValidationError

from mainapp.models import Passport, BaseProduct


class GetProducts(forms.Form):
	products = forms.JSONField()
	response = {}

	def clean_products(self):
		req = self.cleaned_data['products']

		passports: list[dict] = req.get('passports')
		if passports is not None:
			self.response['passports'] = self._get_data_from_db(Passport, passports)

	@staticmethod
	def _get_data_from_db(model: BaseProduct, products: list[dict]) -> list[dict]:
		id_list = []
		for product in products:
			if (_id := product.get('id')) is None:
				raise ValidationError('No product.id provided!')
			id_list.append(_id)

		queryset = model.objects.filter(id__in=id_list).all()

		result = list(p.to_dict() | {'count': product.get('count')} for p in queryset)

		return result

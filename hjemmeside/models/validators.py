from django.core.validators import RegexValidator, MaxValueValidator

kun_tall_validator = RegexValidator(r'^\d+$', 'Kun tillatt med tall. Fjern tomrom.')
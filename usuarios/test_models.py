import pytest
from django.core.exceptions import ValidationError
from usuarios.models import User, Unid_Org


@pytest.mark.django_db
def test_usuario_con_campos_no_validos():
    unidad = Unid_Org.objects.create(nombre='Unidad Test', siglas='UT')

    with pytest.raises(ValueError):
        User.objects.create_user(
            username='',
            password='password123',
            email='testuser@example.com',
            phone_number='1234567890',
            role='admin',
            unidad=unidad
        )

    with pytest.raises(ValidationError):
        usuario = User(
            username='invalid_email_user',
            email='no_es_un_email',
            phone_number='1234567890',
            role='admin',
            unidad=unidad
        )
        usuario.full_clean()

    with pytest.raises(ValidationError):
        usuario = User(
            username='invalid_role_user',
            email='validemail@example.com',
            phone_number='1234567890',
            role='not_a_valid_role',
            unidad=unidad
        )
        usuario.full_clean()

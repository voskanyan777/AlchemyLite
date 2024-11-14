import pytest


def test_update_by_id(sync_crud):
    sync_crud.update_by_id(id=1, name='new_test', email='<EMAIL>')
    result = sync_crud.read_by_id(id=1)
    result = result[0]
    assert result['id'] == 1
    assert result['name'] == 'new_test'
    assert result['email'] == '<EMAIL>'


def test_update_by_id_with_exception(sync_crud):
    with pytest.raises(ValueError, match='Parameter "id" must be an integer'):
        sync_crud.update_by_id(id='id', name='new_test', email='<EMAIL>')


def test_update_by_id_with_id_missing(sync_crud):
    with pytest.raises(ValueError, match='Parameter "id" is missing'):
        sync_crud.update_by_id(name='new_test', email='<EMAIL>')


def test_update_by_id_with_incorrect_params(sync_crud):
    with pytest.raises(ValueError, match='Parameter year is not a valid column name'):
        sync_crud.update_by_id(name='test', email='<EMAIL>', year='year')
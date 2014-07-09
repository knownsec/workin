#!/usr/bin/env python
# coding: utf-8

from workin.exceptions import ConfigError


class AdminAction(object):
    pass


class AdminBulkAction(AdminAction):
    @classmethod
    def process_list_choices(cls, *args, **kwargs):
        raise ConfigError('%s should implement process_list_choices method' % cls.__name__)


class BulkDeleteAction(AdminBulkAction):
    @classmethod
    def process_list_choices(cls, db, model, id_list):
        db.query(model).filter(model.id.in_(id_list)).delete(synchronize_session='fetch')
        db.commit()


class EditAction(AdminAction):
    url_name = 'admin_edit'
    label = 'Edit'


class DeleteAction(AdminAction):
    url_name = 'admin_edit'
    label = 'Delete'


class DetailAction(AdminAction):
    url_name = 'admin_detail'
    label = 'Detail'


BULK_ACTIONS_MAP = {
    'delete': BulkDeleteAction,
}

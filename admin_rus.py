from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.utils.text import get_text_list

    
class AdminRusMixin(object):
    def construct_change_message(self, request, form, formsets):
        """
        Construct a change message from a changed object.
        """

        def get_trans_text_list(list_, last_word, prefix='"', postfix='"',
                                instance=None):
            def get_field_name(field_name):
                try:
                    return instance.__class__._meta.get_field(field_name).verbose_name
                except:
                    return field_name

            return get_text_list(
                [''.join([prefix, str(get_field_name(i)), postfix]) for i in list_],
                last_word
            )

        change_message = []
        if form.changed_data:
            change_message.append(_('Changed %s.') % get_trans_text_list(
                form.changed_data, _('and'), instance=getattr(form, 'instance', None) 
            ))

        if formsets:
            for formset in formsets:
                for added_object in formset.new_objects:
                    change_message.append(_('Added %(name)s "%(object)s".')
                                          % {'name': force_text(added_object._meta.verbose_name),
                                             'object': force_text(added_object)})
                for changed_object, changed_fields in formset.changed_objects:
                    change_message.append(_('Changed %(list)s for %(name)s "%(object)s".')
                                          % {'list': get_trans_text_list(
                                                changed_fields, _('and'), instance=changed_object
                                             ),
                                             'name': force_text(changed_object._meta.verbose_name),
                                             'object': force_text(changed_object)})
                for deleted_object in formset.deleted_objects:
                    change_message.append(_('Deleted %(name)s "%(object)s".')
                                          % {'name': force_text(deleted_object._meta.verbose_name),
                                             'object': force_text(deleted_object)})
        change_message = ' '.join(change_message)
        return change_message or _('No fields changed.')

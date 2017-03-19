from collections import OrderedDict

from django.db import models
from django.db.models.functions import Lower
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject


class FilteredReverseRelationSerializer(serializers.ModelSerializer):
    def apply_user_reverse_relation_filters(self, queryset, request, parent):
        return queryset

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if isinstance(attribute, models.Manager):
                    attribute = attribute.all()

                    attribute = self.apply_user_reverse_relation_filters(attribute, self.context.get('request'),
                                                                         instance)

                    if 'view' in self.context:
                        if self.context['view'].search_fields and \
                                'request' in self.context and self.context['request'].GET.get('search'):

                            search = self.context['request'].GET.get('search')

                            search_fields = filter(lambda x: field.field_name + '__' in x, self.context['view'].search_fields)

                            for search_field in search_fields:
                                search_field = search_field.replace(field.field_name + '__', '')
                                search_param = '__icontains'
                                attribute = attribute.filter(**{search_field + search_param: search})

                        if self.context['view'].ordering_fields and \
                                'request' in self.context and self.context['request'].GET.get('ordering'):

                            ordering = self.context['request'].GET.get('ordering')

                            ordering = ordering.replace(field.field_name + '__', '')
                            if ordering.startswith('-'):
                                attribute = attribute.order_by(Lower(ordering[1:]).desc())
                            else:
                                attribute = attribute.order_by(ordering)

                ret[field.field_name] = field.to_representation(attribute)

        return ret
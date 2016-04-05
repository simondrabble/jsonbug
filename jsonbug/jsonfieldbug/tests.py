from django.test import TestCase


from . import models


class TestSerialization(TestCase):

    def test_serialization(self):
        data = {'test': 42, 'pi': 3.14}
        item = models.JsonSerializationBug(data=data)
        item.save()

        self.assertIsNotNone(item.pk)

        retrieved = models.JsonSerializationBug.objects.get(pk=item.pk)
        self.assertEqual(data, retrieved.data)

        # The below fails since the data is serialized as
        # sqlite> select * from jsonfieldbug_jsonserializationbug;
        # 1|"{'test': 42, 'pi': 3.14}"
        # (Note the "" characters that are part of the serialized data)
        #
        # While the query to retrieve it is:
        #
        # SELECT "jsonfieldbug_jsonserializationbug"."id", "jsonfieldbug_jsonserializationbug"."data"
        # FROM "jsonfieldbug_jsonserializationbug"
        # WHERE "jsonfieldbug_jsonserializationbug"."data" = "{'test': 42, 'pi': 3.14}"
        #
        # Note the missing escapes for the outer quote characters - IOW, the
        # query is attempting to perform a search for the literal value
        # {'test': 42, 'pi': 3.14}
        # without the double-quotes present in the serialized string.
        #
        # The fix is to cwcorrectly quote the data parameter:
        # SELECT "jsonfieldbug_jsonserializationbug"."id", "jsonfieldbug_jsonserializationbug"."data"
        # FROM "jsonfieldbug_jsonserializationbug" WHERE
        # "jsonfieldbug_jsonserializationbug"."data" = '"{''test'': ''str''}"';

        retrieved = models.JsonSerializationBug.objects.get(data=data)
        self.assertEqual(item.pk, retrieved.pk)

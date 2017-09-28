from django.test import TestCase
from trello.models import *


# Create your tests here.


class ModelsTestCase(TestCase):
    def setUp(self):
        listTest = List.objects.create(name="list test")
        Card.objects.create(
            name="card test",
            description="testing card",
            list=listTest
        )

    def test_is_created_properly(self):
        listTest = List.objects.get(name="list test")
        card = Card.objects.get(name="card test")
        self.assertEqual(listTest.card_set.all().count(), 1)
        self.assertEqual(card.list.name, "list test")


class ListTest(TestCase):
    def test_list_func(self):
        # index
        response = self.client.get('/trello/')
        self.failUnlessEqual(response.status_code, 200)

        # create a list - result: list -1

        response = self.client.post("/trello/create_list", {"name": "test"})
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(List.objects.latest('id').name, "test")

        # create a card - result: list -1, card -1
        response = self.client.post("/trello/create_card", {"name": "test cards",
                                                            "description": "test cards",
                                                            "list": List.objects.latest('id').id
                                                            })
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(Card.objects.latest('id').name, "test cards")
        self.assertEqual(Card.objects.all().count(), 1)

        # copy list - result: lists -2, cards -2

        response = self.client.post("/trello/copy_list/" + str(List.objects.latest('id').id))
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(List.objects.all().count(), 2)
        self.assertEqual(Card.objects.all().count(), 2)

        # creating one more card and  delete all cards - result: lists -2, cards -1
        response = self.client.post("/trello/create_card", {"name": "test cards",
                                                            "description": "test cards",
                                                            "list": List.objects.latest('id').id
                                                            })
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(Card.objects.latest('id').name, "test cards")

        # created one more card result: cards-2
        self.assertEqual(Card.objects.all().count(), 3)

        # deleting all cards in latest list - result: lists-2 cards-1
        response = self.client.post("/trello/delete_allcards/" + str(List.objects.latest('id').id))

        self.assertEqual(List.objects.latest('id').card_set.all().count(), 0)
        self.assertEqual(List.objects.all().count(), 2)
        self.assertEqual(Card.objects.all().count(), 1)
        self.failUnlessEqual(response.status_code, 200)

        # creating card one more tiem and then deleting list with cards - result: list -1, card -1
        response = self.client.post("/trello/create_card", {"name": "test cards",
                                                            "description": "test cards",
                                                            "list": List.objects.latest('id').id
                                                            })
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(Card.objects.latest('id').name, "test cards")
        #checking if card created
        self.assertEqual(Card.objects.all().count(), 2)

        # deleting a list with latest id and its cards
        response = self.client.post("/trello/delete_list/" + str(List.objects.latest('id').id))
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(Card.objects.all().count(), 1)
        self.assertEqual(List.objects.all().count(), 1)

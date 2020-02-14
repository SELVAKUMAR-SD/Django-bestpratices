from django.test import TestCase


class TestUserRoutes(TestCase):
    """
    Testing For User Endpoint's
    """

    def test_user_signup(self):
        """
        Test user signup
        :return: 201
        """
        response = self.client.post('users/signup/',
                                    data=dict(firtst_name='prime',
                                              last_name='prime',
                                              email='selvakumar@gmail.com',
                                              password='iphone21',
                                              phone_no='9655952778'))
        print(response)

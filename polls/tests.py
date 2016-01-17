import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question

# Create your tests here.
class QuestionMethodTests(TestCase):
	def test_recent_with_future_q(self):
		"""
		recent() should return False for questions whose pub_date is in the future
		"""
		time = timezone.now()+datetime.timedelta(days=30)
		future_q = Question(pub_date=time)

		self.assertEqual(future_q.recent(), False)

	def test_recent_with_old_q(self):
		"""
		recent() should return False for questions older than a day
		"""
		time = timezone.now()-datetime.timedelta(days=2)
		old_q = Question(pub_date=time)

		self.assertEqual(old_q.recent(), False)

	def test_recent_with_recent_q(self):
		"""
		recent() should return True for questions published in the last day
		"""
		time = timezone.now()-datetime.timedelta(hours=6)
		recent_q = Question(pub_date=time)

		self.assertEqual(recent_q.recent(), True)


class QuestionViewTests(TestCase):
	def create_question(question_text, days):
		"""
		Creates a question with the given `question_text` and published the
		given number of `days` offset to now (negative for questions published
		in the past, positive for questions that have yet to be published).
		"""
		time=timezone.now() + datetime.timedelta(days=days)
		return Question.objects.create(question_text=question_text, pub_date = time)

	def test_index_view_with_no_qs(self):
		"""
    If no questions exist, an appropriate message should be displayed.
    """
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'],[])

  def test_index_view_future_and_past_q(self):
  	"""
    Even if both past and future questions exist, only past questions
    should be displayed.
    """
    create_question(question_text="Past question", days =-30)
    create_question(question_text="Future question", days=30)
    response=self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context
    	['latest_question_list'],['<Question: Past question.>']
    	)


class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_future_q(self):
		"""
		The detail view of a question with a pub_date in the future should
		return a 404 not found.
		"""
		future_q=create_question(question_text='Future Question', days=5)
		response=self.client.get(reverse('polls:detail',
			args=(future_q.id,)))
		self.assertEqual(response.status_code, 404)
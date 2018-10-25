from nameko.rpc import rpc
from shared_utils.logger import EntrypointLogger, _log
from review_service.review_service_file import ReviewService

class Review_Nameko_api:

    name = 'review_service'
    entrypoint_logger = EntrypointLogger()

    review_service = ReviewService()

    @rpc
    def get_all_reviews(self):
        return self.review_service.get_all_reviews()

    @rpc
    def get_tape_reviews(self, tape_id):
        return self.review_service.get_tape_reviews(tape_id)

    @rpc
    def get_user_reviews(self, user_id):
        return self.review_service.get_user_reviews(user_id)
    @rpc
    def get_review(self, tape_id, user_id):
        return self.review_service.get_review(tape_id, user_id)



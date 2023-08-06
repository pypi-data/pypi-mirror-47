from flask_pundit.application_policy import ApplicationPolicy


class CommentingPolicy(ApplicationPolicy):
    def get(self):
        return self.user.get('role') == 'admin'

    def scope(self):
        if self.user.get('role') == 'admin':
            return ['Hello']
        return ['World']

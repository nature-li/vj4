from vj4.model import builtin


class Error(Exception):
  pass


class HashError(Error):
  pass


class InvalidStateError(Error):
  pass


class UserFacingError(Error):
  """Error which faces end user."""

  def to_dict(self):
    return {'name': self.__class__.__name__, 'args': self.args}

  @property
  def http_status(self):
    return 500

  @property
  def template_name(self):
    return 'error.html'

  @property
  def message(self):
    return 'An error has occurred.'


class BadRequestError(UserFacingError):
  @property
  def http_status(self):
    return 400


class ForbiddenError(UserFacingError):
  @property
  def http_status(self):
    return 403


class NotFoundError(UserFacingError):
  @property
  def http_status(self):
    return 404

  @property
  def message(self):
    return 'Path {0} not found.'


class BuiltinDomainError(ForbiddenError):
  @property
  def message(self):
    return 'Domain {0} is bulit-in and cannot be modified.'


class ValidationError(ForbiddenError):
  @property
  def message(self):
    if len(self.args) == 1:
      return 'Field {0} validation failed.'
    elif len(self.args) == 2:
      return 'Field {0} or {1} validation failed.'


class BlacklistedError(ForbiddenError):
  @property
  def message(self):
    return 'Address {0} is blacklisted.'


class FileTooLongError(ValidationError):
  @property
  def message(self):
    return 'The uploaded file is too long.'


class FileTypeNotAllowedError(ValidationError):
  @property
  def message(self):
    return 'This type of files are not allowed to be uploaded.'


class UnknownFieldError(ForbiddenError):
  @property
  def message(self):
    return 'Unknown field {0}.'


class InvalidTokenError(ForbiddenError):
  pass


class VerifyPasswordError(ForbiddenError):
  """Error with the `verify password', not password verification error."""
  @property
  def message(self):
    return "Passwords don't match."


class UserAlreadyExistError(ForbiddenError):
  @property
  def message(self):
    return 'User {0} already exists.'


class UserNotExistError(ForbiddenError):
  @property
  def message(self):
    return 'User {0} not exists.'


class LoginError(ForbiddenError):
  @property
  def message(self):
    return 'Invalid password for user {0}.'


class DocumentNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'Document {2} not found.'


class ProblemDataNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'Data of problem {1} not found.'


class RecordDataNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'Data of record {0} not found.'


class PermissionError(ForbiddenError):
  def __init__(self, *args):
    super().__init__(*args)
    if any((p | builtin.PERM_VIEW) == builtin.PERM_VIEW for p in self.args):
      self.__message = 'You cannot visit this domain.'
    else:
      self.__message = "You don't have the required permission ({0}) in this domain."
      if len(self.args) > 0 and self.args[0] in builtin.PERMS_BY_KEY:
        self.args = (builtin.PERMS_BY_KEY[self.args[0]].desc, self.args[0], *self.args[1:])

  @property
  def message(self):
    return self.__message


class PrivilegeError(ForbiddenError):
  @property
  def message(self):
    if any((p | builtin.PRIV_USER_PROFILE) == builtin.PRIV_USER_PROFILE for p in self.args):
      return "You're not logged in."
    else:
      return "You don't have the required privilege."


class CsrfTokenError(ForbiddenError):
  pass


class InvalidOperationError(ForbiddenError):
  pass


class AlreadyVotedError(ForbiddenError):
  @property
  def message(self):
    return "You've already voted."


class UserNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'User {0} not found.'


class InvalidTokenDigestError(ForbiddenError):
  pass


class CurrentPasswordError(ForbiddenError):
  @property
  def message(self):
    return "Current password doesn't match."


class DiscussionCategoryAlreadyExistError(ForbiddenError):
  @property
  def message(self):
    return 'Discussion category {1} already exists.'


class DiscussionCategoryNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'Discussion category {1} not found.'


class DiscussionNodeAlreadyExistError(ForbiddenError):
  @property
  def message(self):
    return 'Discussion node {1} already exists.'


class DiscussionNodeNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'Discussion node {1} not found.'


class DiscussionNotFoundError(DocumentNotFoundError):
  @property
  def message(self):
    return 'Discussion {1} not found.'


class MessageNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'Message {0} not found.'


class DomainNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'Domain {0} not found.'


class DomainAlreadyExistError(ForbiddenError):
  @property
  def message(self):
    return 'Domain {0} already exists.'


class DomainJoinForbiddenError(ForbiddenError):
  @property
  def message(self):
    return 'You are not allowed to join the domain. The link is either invalid or expired.'


class DomainJoinAlreadyMemberError(ForbiddenError):
  @property
  def message(self):
    return 'Failed to join the domain. You are already a member.'


class InvalidJoinInvitationCodeError(ForbiddenError):
  @property
  def message(self):
    return 'The invitation code you provided is invalid.'


class ContestAlreadyAttendedError(ForbiddenError):
  @property
  def message(self):
    return "You've already attended this contest."


class ContestNotAttendedError(ForbiddenError):
  @property
  def message(self):
    return "You haven't attended this contest yet."


class ContestScoreboardHiddenError(ForbiddenError):
  @property
  def message(self):
    return 'Contest scoreboard is not visible.'


class ContestNotLiveError(ForbiddenError):
  @property
  def message(self):
    return 'This contest is not live.'


class HomeworkScoreboardHiddenError(ForbiddenError):
  @property
  def message(self):
    return 'Homework scoreboard is not visible.'


class HomeworkNotLiveError(ForbiddenError):
  @property
  def message(self):
    return 'This homework is not open.'


class HomeworkAlreadyAttendedError(ForbiddenError):
  @property
  def message(self):
    return "You've already claimed this homework."


class HomeworkNotAttendedError(ForbiddenError):
  @property
  def message(self):
    return "You haven't claimed this homework yet."


class ProblemNotFoundError(DocumentNotFoundError):
  @property
  def message(self):
    return 'Problem {1} not found.'


class TrainingRequirementNotSatisfiedError(ForbiddenError):
  @property
  def message(self):
    return 'Training requirement is not satisfied.'


class TrainingAlreadyEnrollError(ForbiddenError):
  @property
  def message(self):
    return "You've already enrolled this training."


class RecordNotFoundError(NotFoundError):
  @property
  def message(self):
    return 'Record {0} not found.'


class OpcountExceededError(ForbiddenError):
  @property
  def message(self):
    return 'Too frequent operations of {0} (limit: {2} operations in {1} seconds).'


class UsageExceededError(ForbiddenError):
  @property
  def message(self):
    return 'Usage exceeded.'


class DomainRoleAlreadyExistError(ForbiddenError):
  @property
  def message(self):
    return 'Role {1} already exists in domain {0}.'


class ModifyBuiltinRoleError(ForbiddenError):
  @property
  def message(self):
    return 'Built-in roles cannot be modified.'


class UserAlreadyDomainMemberError(ForbiddenError):
  @property
  def message(self):
    return 'The user is already a member of the domain.'


class InvalidArgumentError(BadRequestError):
  @property
  def message(self):
    return 'Argument {0} is invalid.'


class NoProblemError(NotFoundError):
  @property
  def message(self):
    return 'No problem.'


class BatchCopyLimitExceededError(ForbiddenError):
  @property
  def message(self):
    return 'Only {0} problems can be copied in one request, got {1}.'


class UpgradeLockAcquireError(Error):
  @property
  def message(self):
    return 'Failed to acquire the upgrade lock. There may be another ongoing upgrade process, or a previous process is exited unexpectedly.'


class UpgradeLockReleaseError(Error):
  @property
  def message(self):
    return 'Failed to release the upgrade lock. The database is malformed during the upgrade.'


class DatabaseVersionMismatchError(Error):
  @property
  def message(self):
    return 'Database version mismatch, got {0}, expect {1}. You need to invoke database upgrades.'


class SendMailError(UserFacingError):
  @property
  def message(self):
    return 'Failed to send mail to {0}.'

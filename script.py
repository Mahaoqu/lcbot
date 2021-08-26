
from data import Problem

greeting = 'Hello {}! '
submit = 'You have checked-in a leetcode problem <{}|#{} {}>. '

submit_easy = 'Good job! '
submit_medium = 'You have accomplished a feat! '
submit_hard = "I can't believe you finally did it! "

submit_after = 'Can any else do that?'
submit_first_of_day = ''
submit_when_too_many = ''
submit_topic_dynamic_programming = ''

no_submit_today = 'You have not submit your problems today.'


def get_submit_script(p: Problem, name: str) -> str:
    script = ''
    script += greeting.format(name)
    script += submit.format(p.url, p.id, p.title)

    # choose script by difficulty
    if p.difficulty == 'Easy':
        script += submit_easy
    elif p.difficulty == 'Medium':
        script += submit_medium
    elif p.difficulty == 'Hard':
        script += submit_hard
    else:
        raise Exception("problem difficulty error")

    # Message Format In 
    # https://api.slack.com/methods/chat.postMessage
    # and
    # https://api.slack.com/reference/surfaces/formatting
    return script

import unittest
from quasimodo.statement_maker import StatementMaker

dataset = [
    ("why is", "is", ""),
    ("how is software piracy illegal in the first place?", "software", 'software piracy is illegal in the first place'),
    ("why are white monkeys superior to other races?", "white", 'white monkeys are superior to other races'),
    ("why can nebraska recruit?", "nebraska", 'nebraska can recruit'),
    ("why do nebraska recruit?", "nebraska", 'nebraska recruit'),
    ("how are weed vans legal in atlanta, ga?", "weed", "weed vans are legal in atlanta, ga"),
    ("how are gold nano-particles colored", "gold", "gold nano-particles are colored"),
    # ("how are other ents preparing for secret santa", "other", 'other ents are preparing for secret santa'),
    ("how are pumpkin pies are made", "pumpkins", "pumpkin pies are made"),
    ("why are black monkeys killers", "black", "black monkeys are killers"),
    ("why is black a color", "black", "black is a color"),
    ("why cant Leeds get promoted", "leeds", 'leeds can get promoted'),
    ("why are client profitability studies important", "client", 'client profitability studies are important'),
    # ("why are plasma thrusters so hard to create", "plasma", 'plasma thrusters are so hard to create'),
    ("why can cold dark matter simply be h2 gas", "cold", 'cold dark matter simply can be h2 gas'),
    ("why is becoming a nurse so hard", "becoming", "becoming a nurse is so hard"),
    ("how was math created", "math", "math was created"),
    ("why is light crude oil more expensive in summer in the northern hemisphere", "light",
     "light crude oil is more expensive in summer in the northern hemisphere"),
    ("why is egypt at war with israel", "egypt", 'egypt is at war with israel'),
    ("why are cactus spiky", "egypt", 'cactus are spiky'),
    ("why are canadians are in russia cold", "canadian", 'canadians in russia are cold'),
    ("why are canada and russia colder than the uk", "canada", 'canada and russia are colder than the uk'),
    ("why are pink and grey elephants big and fat", "pink", "pink and grey elephants are big and fat"),
     ("why are pink flamingo and gray elephant big and fat", "flamingos",
      "pink flamingo and gray elephant are big and fat"),
    ("why are pink flamingos big and fat", "flamingo", "pink flamingos are big and fat"),
    ("why are butts pink", "butts", "butts are pink"),
    ("why is ice floating", "float", 'ice is floating'),
    ("why are cactus bad luck", "cactus", 'cactus are bad luck'),
    ("why are cactus so lucky", "cactus", "cactus are so lucky"),
    ("why are there cactus in africa", "cactus", "there are cactus in africa"),
    ("why is it cold in africa", "cactus", 'it is cold in africa'),
    ("why is kale not allowed on dr bernstein", "kale", 'kale is not allowed on dr bernstein'),
    ("why is tom's idea good?", "tom", "tom's idea is good"),
    ("why are elephants big while i am small", "elephants", 'elephants are big while i am small'),
    ("why is chocolate of switzerland better", "chocolate", "chocolate of switzerland is better"),
    ("why is chocolate in the north of switzerland better", "switzerland",
     "chocolate in the north of switzerland is better"),
    ("why are lily pads zipping", "lily pad", "lily pads are zipping"),
    ("why does panda climb tree", "panda", "panda climb tree"),
    ("why do african people have noses and lips", "african people", "african people have noses and lips"),
    ("why are african elephants endangered", "elephant", "african elephants are endangered"),
    ("why elephants are big", "elephant", "elephants are big")
]


class TestStatementMaker(unittest.TestCase):

    def setUp(self) -> None:
        self.statement_maker = StatementMaker(use_cache=False)

    def test_dataset(self):
        for question, subject, statement in dataset:
            self.assertEqual(statement, self.statement_maker.to_statement(question, subject))

    def _test_temp(self):
        for question, subject, statement in [("why are lily pads zipping", "lily pad", "lily pads are zipping")]:
            self.assertEqual(statement, self.statement_maker.to_statement(question, subject))


if __name__ == '__main__':
    unittest.main()

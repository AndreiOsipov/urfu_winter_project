class ChoicesGenerator:
    def generate_tuple(self, value, required_float = False):
        return (value, f'до {value}')
    
    def generate_choices(self, start, end, step):
        choices = []

        for i in range(start, end, step):
            choices.append((i,f'до {float(i+1)}'))

        return choices


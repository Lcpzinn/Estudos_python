import random

piadas = [
    "Por que o livro de matemática se suicidou? Porque tinha muitos problemas.",
    "O que o zero disse para o oito? Belo cinto!",
    "Qual é o cúmulo da paciência? Jogar xadrez sozinho e esperar a sua vez.",
    "Por que o jacaré tirou o filho da escola? Porque ele mandava muito mal na matéria de rios.",
    "O que é um ponto verde no canto da sala? Um ervilha de castigo."
]

print(random.choice(piadas))

numeros= [2, 33, 43, 89]

print("Números sorteados:", random.sample(numeros, 2))
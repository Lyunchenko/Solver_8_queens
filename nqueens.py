import random

class Solver_8_queens:
	"""Решение задачи о 8 ферзях"""

	def __init__(self, pop_size = 45, cross_prob = 0.70, mut_prob = 0.20):
		self.pop_size = pop_size
		self.cross_prob = cross_prob
		self.mut_prob = mut_prob

	def solve(self, min_fitness = 1, max_epochs = 300):
		"""Поиск решения
			| Значие фитнес-функции варьируется от 0 до 1 
			| (1 - верное решение, 0,03 - решение с 1 ошибкой)""" 
		self.pop = POPULATION(inPopulationSize = self.pop_size, inChanceCrossing = self.cross_prob, inChanceMutation = self.mut_prob)
		while self.pop.epoch < max_epochs and not self.pop.CheckBestPerson(min_fitness):
			self.pop.NextEpoch()
		self.bestPerson = self.pop.GetBestPerson()
		self.answer = (self.bestPerson.valueFitnes, self.pop.epoch ,self.bestPerson.GetString())
		return(self.answer)

class POPULATION:
	"""Популяция особей
		| Конструктор: размер популяции, вероятность скрещивания, вероятность мутации
		| GetAvgFitFunc - среднее значение фитнес-функции
		| GetTrueAnswer - проверка наличия правильного решения (возвращает хромосому или False)
		| GetBestPerson - получение лучшей особи в популяции
		| GetSumFitFunc - получить сумму фитнес функций
		| NextEpoch - следующая эпоха"""

	def __init__(self, inPopulationSize = 45, inChanceCrossing = 0.70, inChanceMutation = 0.20, inExp = 5):
		
		# Получение входных параметров
		self.populationSize = inPopulationSize
		self.chanceCrossing = inChanceCrossing
		self.chanceMutation = inChanceMutation

		# Определение дополнительных параметров
		self.boardSize = 8
		self.objFitnesFunction = FITNESS_FUNCTION(self.boardSize)
		self.sizeChrom = 8
		self.exp = inExp

		# Генерация первичной популяции
		self.GetPersons()
		#while self.GetAvgFitFunc() <= 0.002:
		#	self.GetPersons()

		# Счетчик эпох
		self.epoch = 1

	def GetPersons(self):
		"""Генерация первичной популяции"""
		self.persons = [PERSON(inObjFitnesFunction = self.objFitnesFunction, inSizeChrom = self.sizeChrom, inExp = self.exp)]
		self.ind = 0
		while self.ind < self.populationSize - 1:
			self.ind += 1
			self.persons += [PERSON(inObjFitnesFunction = self.objFitnesFunction, inSizeChrom = self.sizeChrom, inExp = self.exp)]

	def GetAvgFitFunc(self):
		"""Получение среднего значения фитнес функции популяции"""
		self.avgFitFunc = 0
		for x in self.persons:
			self.avgFitFunc += x.valueFitnes
		self.avgFitFunc = self.avgFitFunc / self.populationSize
		return(self.avgFitFunc)

	def GetSumFitFunc(self):
		"""Получение суммы значений фитнес функции популяции"""
		self.sumFitFunc = 0
		for x in self.persons:
			self.sumFitFunc += x.valueFitnes
		return(self.sumFitFunc)

	def GetBestPerson(self):
		"""Получение лучшей особи"""
		self.bestFit = 0
		for x in self.persons:
			if x.valueFitnes > self.bestFit:
				self.bestFit = x.valueFitnes
				self.answer = x
		return(self.answer)

	def GetTrueAnswer(self):
		"""Проверка наличия решения в текущей популяции"""
		self.Check = False
		for x in self.persons:
			if x.valueFitnes == 1:
				self.Check = x
				break
		return(self.Check)

	def CheckBestPerson(self, min_fitness):
		"""Проверка превышения порогового значения фитнес-функции"""
		self.Check = False
		for x in self.persons:
			if x.valueFitnes >= min_fitness:
				self.Check = True
				break
		return(self.Check)

	def NextEpoch(self):
		"""Переход в следующую эпоху"""
		self.Selection()
		self.Crossing()
		self.Mutation() 
		self.epoch += 1
	
	def Selection(self):
		"""Отбор особей для скрещивания"""
		self.sumFitFunc = self.GetSumFitFunc()
		self.selectP = None
		for x in self.persons:
			self.chromCount = round(self.populationSize * x.valueFitnes / self.sumFitFunc)
			self.ind = 0
			while self.ind < self.chromCount:
				self.ind += 1
				self.selectP = [x] if self.selectP == None else self.selectP + [x]

	def Crossing(self):
		"""Скрещивание особей"""
		self.ind = self.populationSize
		self.persons = None
		while self.ind != 0:
			if self.GetChance(self.chanceCrossing):
				# Скрещивание особей
				self.Check = True
				while self.Check:
					self.idPerson1 = random.randint(0, len(self.selectP) - 1)
					self.idPerson2 = random.randint(0, len(self.selectP) - 1)
					self.childPerson = False
					if self.idPerson1 != self.idPerson2:
						self.childPerson = self.selectP[self.idPerson1].Crossing(self.selectP[self.idPerson2])
					if self.childPerson != False:
						if self.ind != 0:
							self.persons = [self.childPerson[0]] if self.persons == None else self.persons + [self.childPerson[0]] 
							self.ind -= 1
						if self.ind != 0:
							self.persons += [self.childPerson[1]] 
							self.ind -= 1
						self.Check = False
			else:
				# Хромосомы не скрещиваются, переносятся в популяцию
				if self.ind != 0:
					self.idPerson = random.randint(0, len(self.selectP) - 1)
					self.persons = [self.selectP[self.idPerson]] if self.persons == None else self.persons + [self.selectP[self.idPerson]]
					self.ind -= 1
				if self.ind != 0:
					self.idPerson = random.randint(0, len(self.selectP) - 1)
					self.persons += [self.selectP[self.idPerson]]
					self.ind -= 1

	def Mutation(self):
		"""Мутация особей с заданной вероятностью"""
		for x in self.persons:
			if self.GetChance(self.chanceMutation): 
				x.Mutation()

	def GetChance(self, chance):
		"""Исполненеи вероятносного события"""
		if random.randint(1, 100) <= chance * 100: self.answer = True
		else: self.answer = False
		return(self.answer)

class PERSON:
	"""Класс для экземляра одной особи
		| Конструктор: объект фитнес-функции, хромосома особи, размер хромосомы, размер доски
		| valueFitnes - значение фитнес-функции для текущей хромосомы особи
		| Mutation - случайное изменение одного из значений в хромосоме
		| Crossing - скрещивание хромосом 2-х особей"""

	def __init__(self, inObjFitnesFunction = None, inChrom = None, inSizeChrom = 8, inBoardSize = 8, inExp = 5):
		
		if inObjFitnesFunction == None:
			self.boardSize = inBoardSize
		else:
			self.boardSize = inObjFitnesFunction.boardSize 
		
		self.objFitnesFunction = FITNESS_FUNCTION(self.boardSize) if inObjFitnesFunction == None else inObjFitnesFunction
		
		if inChrom == None:
			self.sizeChrom = inSizeChrom
		else:
			self.sizeChrom = len(inChrom)
		
		self.chromosome = self.GetChromosome() if inChrom == None else inChrom
		self.exp = inExp

		self.GetValueFitnes()


	def GetChromosome(self):
		"""Генерация случайной хромосомы"""
		
		self.maxInd = self.boardSize ** 2
		self.chromosome = [random.randint(1, self.maxInd)]
		self.ind = 0
		while self.ind < self.sizeChrom - 1:
			self.ind += 1
			self.checkDuplicates = True
			while self.checkDuplicates:
				self.checkDuplicates = False
				self.mRnd = random.randint(1, self.maxInd)
				for x in self.chromosome:
					if x == self.mRnd:
						self.checkDuplicates = True
						break
			self.chromosome += [self.mRnd]
		return(self.chromosome)
		
	def GetValueFitnes(self):
		"""Получение фитнес-функции для текущей хромосомы особи""" 
		self.valueFitnes = self.objFitnesFunction.GetValueFitnes(self.chromosome, self.exp)

	def GetString(self):
		"""Получение строки визуализации решения"""
		self.string = None 
		self.i = 0
		while self.i < 64:
			self.i += 1
			self.char = '+'
			for x in self.chromosome:
				if x == self.i: self.char = 'Q'
			self.string = self.char if self.string == None else self.string + self.char
			if self.i % 8 == 0: self.string += '\n'
		return(self.string)
	
	def Mutation(self):
		"""Мутация - случайное изменение одного из значений хромосомы"""
		self.maxInd = self.boardSize ** 2
		while True:
			self.tempChrom = list(self.chromosome) # простое присваивание передает ссылку на список!
			self.mRnd = random.randint(0, self.sizeChrom-1)
			self.tempChrom[self.mRnd] = random.randint(1, self.maxInd)
			if self.CheckCrom(self.tempChrom): break
		self.chromosome = self.tempChrom
		self.GetValueFitnes()

	def Crossing(self, objCross):
		"""Скрещивание хромосом 2-х особей
			| Вход: объект PERSON для скрещивания
			| Выход: список из 2-х хромосом или False если крещивание не дает корректного результата"""
		# Формирование скрещенных хромосом
		self.ind = 0
		self.childChrom = False
		while self.ind < self.sizeChrom * 2:
			self.ind += 1
			self.mRnd = random.randint(1, self.sizeChrom-1)
			self.childChrom = [self.chromosome[0:self.mRnd] + objCross.chromosome[self.mRnd:]]
			self.childChrom += [objCross.chromosome[0:self.mRnd] + self.chromosome[self.mRnd:]]
			if self.CheckCrom(self.childChrom[0]) and self.CheckCrom(self.childChrom[1]) : break
			self.childChrom = False
		# Создание объектов особей с полученными хромосомами
		if self.childChrom == False:
			self.childPerson = False
		else:
			self.childPerson = [PERSON(inObjFitnesFunction = self.objFitnesFunction, inChrom = self.childChrom[0], inExp = self.exp)]
			self.childPerson += [PERSON(inObjFitnesFunction = self.objFitnesFunction, inChrom = self.childChrom[1], inExp = self.exp)]
		return(self.childPerson)

	def CheckCrom(self, chrom):
		"""Проверка на отсутствие повторов в хромосоме
		   | Вход: хромосома особи
		   | Выход: True - нет повторов, False - есть повторы"""
		self.checkChrom = 0
		for x in chrom:
			for y in chrom:
				if x == y:
					self.checkChrom += 1
		self.checkChrom = True if self.checkChrom == len(chrom) else False
		return(self.checkChrom)

class FITNESS_FUNCTION:
	"""Класс для расчета фитнес функции
		| Конструктор: размер доски (целое)
		| GetValueFitnes - получить значение фитнес функции """

	def __init__(self, boardSize = 8):
		self.boardSize = boardSize
		self.GetMatrixForSums(boardSize)

	def GetValueFitnes(self, chromosome, exponent = 5):
		"""Получить значение фитнес-функции для хромосомы
			| Вход: хромосома
			| Выход: значение фитнес-функции"""
		# Расчет сумм по матрице индексов для суммирования
		self.mSums = None
		self.i = -1
		for mInd in self.matrixForSums:
			self.mSums = [0] if self.mSums == None else self.mSums + [0]
			self.i += 1
			for x in mInd:
				for q in chromosome:
					if q == x:
						self.mSums[self.i] += 1 
		
		# Расчет фитнес-функции
		self.FFValue = 0
		for x in self.mSums:
			self.FFValue += (x ** exponent)
				# Чем больше степень - тем больше различия между хромосомами
            	# (т.е. хромосомы где есть напремер 3 ферзя в ряд будут сильнее проигрывать тем, где максимум 2 ферзя в ряд)
		self.FFValue -= 31
		self.FFValue = 1/self.FFValue
		return (self.FFValue)

	def GetMatrixForSums(self, boardSize):
		"""Предрасчет списков индексов для быстрого расчета сумм диагоналей, строк и столбцов"""
		# Создание матрицы индексов
		self.i1 = 0
		self.ind = 0
		self.matrixInd = None
		while self.i1 < boardSize:
			self.i1 += 1
			self.i2 = 0
			self.m = None
			while self.i2 < boardSize:
				self.i2 += 1
				self.ind += 1
				self.m = [self.ind] if self.m == None else self.m + [self.ind]
			self.matrixInd = [self.m] if self.matrixInd == None else self.matrixInd + [self.m]	

		# Сбор индексов для суммирования
		# Диагональ 1 до середины
		self.i1 = 0
		self.matrixForSums = None
		while self.i1 <= boardSize-1:
			self.i2 = self.i1
			self.i3 = 0
			self.m = None
			while self.i3 <= self.i1:
				self.m = [self.matrixInd[self.i2][self.i3]] if self.m == None else self.m + [self.matrixInd[self.i2][self.i3]]
				self.i2 -= 1
				self.i3 += 1
			self.matrixForSums = [self.m] if self.matrixForSums == None else self.matrixForSums + [self.m] 
			self.i1 += 1
		# Диагональ 1 после середины
		self.i1 = 1
		while self.i1 <= boardSize-1:
			self.i2 = self.i1
			self.i3 = 7
			self.m = None
			while self.i3 >= self.i1:
				self.m = [self.matrixInd[self.i2][self.i3]] if self.m == None else self.m + [self.matrixInd[self.i2][self.i3]]
				self.i2 += 1
				self.i3 -= 1
			self.matrixForSums += [self.m]
			self.i1 += 1
		# Диагональ 2 после середины
		self.i1 = 0
		while self.i1 <= boardSize-1:
			self.i2 = 0
			self.i3 = self.i1
			self.m = None
			while self.i2 <= boardSize - 1 - self.i1:
				self.m = [self.matrixInd[self.i2][self.i3]] if self.m == None else self.m + [self.matrixInd[self.i2][self.i3]]
				self.i2 += 1
				self.i3 += 1
			self.matrixForSums += [self.m]
			self.i1 += 1
		# Диагональ 2 до середины
		self.i1 = 1
		while self.i1 <= boardSize-1:
			self.i2 = self.i1
			self.i3 = 0
			self.m = None
			while self.i3 <= boardSize - 1 - self.i1:
				self.m = [self.matrixInd[self.i2][self.i3]] if self.m == None else self.m + [self.matrixInd[self.i2][self.i3]]
				self.i2 += 1
				self.i3 += 1
			self.matrixForSums += [self.m]	
			self.i1 += 1
		# Столбцы и строки
		self.i1 = 0
		while self.i1 <= boardSize-1:
			self.matrixForSums += [self.matrixInd[self.i1]]
			self.m = [row[self.i1] for row in self.matrixInd]
			self.matrixForSums += [self.m]
			self.i1 += 1
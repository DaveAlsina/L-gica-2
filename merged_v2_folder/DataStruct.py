from math import sqrt


class SudokuDataStruct():
	def __init__(self, size):
		self.size  = size
		self.data, self.letters = self.datastruct()

	def datastruct(self):
		nums = [n for n in range(self.size)]
		self.No = len(nums)
		datastrc = {}
		letras = []
		
		for n in nums:
			for i in range(self.size):         #codificación para las coordenadas (x,y)
				for j in range(self.size):

					#codifica una coordenada (x,y) en un numero código
					coordCode = self.codifica(i,j,self.size, self.size)          

					"""charCoordCode = chr( coordCode + 256 ) 
					#codifíca en numero código coordenada en una letra"""
	
					numCode = self.codifica( coordCode, n, self.size**2, len(nums) )
					charNumCode = chr( numCode + 256 )
	
					#tupla de número y estado en tablero
					#inicializado a falso por defecto
					datastrc[charNumCode] = False
					letras.append(charNumCode)
	
		return datastrc , letras

	def clearData(self):

		for i in list(self.data.keys()):
			self.data[i] = False


	def codifica(self, f, c, Nf, Nc):
		# Funcion que codifica la fila f y columna c
		
		msg1 = 'Primer argumento incorrecto! Debe ser un numero entre 0 y ' + str(self.size - 1) + "\nSe recibio " + str(f)	
		msg2 = 'Segundo argumento incorrecto! Debe ser un numero entre 0 y ' + str(self.size - 1)  + "\nSe recibio " + str(c)
		assert((f >= 0) and (f <= Nf - 1)), msg1

		assert((c >= 0) and (c <= Nc - 1)), msg2
		
		n = Nc * f + c
		# print(u'Número a codificar:', n)

		return n

	def decodifica(self, n, Nf, Nc): #n es un numero
		# Funcion que codifica un caracter en su respectiva fila f y columna c de la tabla

		msg = 'Codigo incorrecto! Debe estar entre 0 y' + str(self.size * self.size - 1) + "\nSe recibio " + str(n)
		assert((n >= 0) and (n <= Nf * Nc - 1)), msg
 
		f = int(n / Nc)
		c = n % Nc

		return f, c

	def decodificaLetra(self,letra):
		a,num = self.decodifica(ord(letra)-256, self.size**2 , self.No)
		x,y = self.decodifica(a , self.size , self.size)

		return ((x,y), num)

	def valueWrite(self , x , y , num = -1):
	
		if num == -1 :
			for i in range(self.No):
				coordinatesCode = self.codifica(x, y, self.size, self.size)
				numCode = self.codifica( coordinatesCode, i , self.size**2 , self.No)
			
				for j in list(self.data.keys()):
					if j == chr(numCode+256):
						self.data[j] = False

		else:
			coordinatesCode = self.codifica(x, y, self.size, self.size)
			numCode = self.codifica( coordinatesCode, num , self.size**2 , self.No)
			
			for j in list(self.data.keys()):
				if j == chr(numCode+256):
					self.data[j] = True

	def solve(self):
		lst = []
		for i in self.data:
			if self.data[i]== True:
				(x,y),num = self.decodificaLetra(i)
				lst.append(((x,y),num))
			
		return lst

	def coordenadasColumna(self, col):
		helper = []

		for i in range(self.size):
			helper.append((col, i))			

		return helper

	def  coordenadasFila(self, fila):
		helper = []

		for i in range(self.size):
			helper.append((i, fila))

		return helper	

	def coordenadasReg(self, col, fila):
	
		rcol = int( (col)/sqrt(self.size) )
		rfila = int( (fila)/sqrt(self.size) )
		print(col, fila)		

		coordinates = []		
	
		for i in range(int(sqrt(self.size))): 
			for j in range(int(sqrt(self.size))): 
				
				position = ( int(i + sqrt(self.size)*rcol), int(j + sqrt(self.size)*rfila))

				if position == (col, fila):
					continue

				coordinates.append(position)

		return coordinates
	
	def regionRule(self, n):
		
		#decodifica la letra proposicional dada y
		#guarda sus valoes codificados en variables de ayuda
		
		info = self.decodificaLetra(n)
		coordinates = info[0]
		num = info[1]
	
		return self.coordenadasReg(coordinates[0], coordinates[1])


	def columnRule(self, n):
		#decodifica la letra proposicional dada y
		#guarda sus valoes codificados en variables de ayuda

#		print(n)		
		info = self.decodificaLetra(n)
		coordinates = info[0]
		num = info[1]

#		print("coordenadas", coordinates, "numero", num)

		#obtiene las columnas que están alineadas con la de la letra proposicional
		col_coordinates = self.coordenadasColumna(coordinates[0])	

		rule = ""		#guarda la regla proposiconal
		first = True 		#variable centinela para la primera iteración
		
		for i in col_coordinates:
			
			if i == coordinates: 
				continue
			
			coordCode = self.codifica(i[0], i[1],self.size, self.size)          
			"""charCoordCode = chr( coordCode + 256 ) 
			#codifíca en numero código coordenada en una letra"""
	
			numCode = self.codifica( coordCode, num, self.size**2, self.size)
			charNumCode = chr( numCode + 256 )
			
			if(first):
				rule += charNumCode	
				first = False
			else:
				rule += charNumCode  + 'O'

		rule += "-"
		return rule

	
	def rowRule(self, n):
		#decodifica la letra proposicional dada y
		#guarda sus valoes codificados en variables de ayuda
	
#		print(n)
		info = self.decodificaLetra(n)
		coordinates = info[0]
		num = info[1]

		#obtiene las filas que están alineadas con la de la letra proposicional
		row_coordinates = self.coordenadasFila(coordinates[1])	
		rule = ""
		first = True 
		
		for i in row_coordinates:
					
			if i == coordinates: 
				continue

			#print(i, num)
			coordCode = self.codifica(i[0], i[1],self.size, self.size)          
			"""charCoordCode = chr( coordCode + 256 ) 
			#codifíca en numero código coordenada en una letra"""
	
			numCode = self.codifica( coordCode, num, self.size**2, self.size)
			charNumCode = chr( numCode + 256 )
			
			if(first):
				rule += charNumCode	
				first = False
			else:
				rule += charNumCode  + 'O'
 

		rule += "-"
		return rule


	def rules(self): 
		
		rules = []
		rule = "" 

		for i in self.letters: 
			
			#regla de la fila y de la columna juntas con un 'Y'
			rule += self.rowRule(i)	+ self.columnRule(i) + 'Y'
			rules.append(rule)
			rule = ""		
			print(self.regionRule(i))
			print()
		
#		for i in rules:
#			print(i)
#			print()



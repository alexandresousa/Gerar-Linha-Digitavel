
def somaRecursivo(number):
    if len(number) == 1:
        return int(number)

    soma = str(sum([int(char) for char in number]))

    return somaRecursivo(soma)

def proxMultiplo10(number):
    if number%10 == 0:
        return number

    number+=1
    return proxMultiplo10(number)

# Espera receber os campo1, 2 e 3 sem pontos, apenas números.
def criaDV(digitos):

    multiplicadorPar    = 2
    multiplicadorImpar  = 1
    count = 0
    somador = 0

    for digito in digitos[::-1]:

        if count%2 == 0:
            resultadoMultiplicacao = str(int(digito)*multiplicadorPar)

            somador += somaRecursivo(resultadoMultiplicacao)
        else:
            resultadoMultiplicacao = str(int(digito)*multiplicadorImpar)

            somador += somaRecursivo(resultadoMultiplicacao)

        count +=1

    return str(proxMultiplo10(somador) - somador)


def insert_str(string, str_to_insert, index):
  return string[:index] + str_to_insert + string[index:]

def gerar_linha_digitavel(codebar):

  cod_banco 		    = codebar[:3]		  # Identificação do Banco
  cod_moeda 		    = codebar[3:4]		# Código da Moeda (Real = 9, Outras=0)
  dig_verif		      = codebar[4:5]		# Dígito verificador do Código de Barras
  fator_venc		    = codebar[5:9]		# Fator de Vencimento (Vide Nota)
  valor			        = codebar[9:19]	  # Valor
  campo_livre       = codebar[19:44]  # Campo Livre

  # Banco Bradesco
  agencia_benef	    = codebar[19:23]	# Agência Beneficiária (Sem o digito verificador)
  carteira 			    = codebar[23:25]	# Carteira
  num_nosso_num	    = codebar[25:36]	# Número do Nosso Número (Sem o digito verificador)
  conta_benef		    = codebar[36:43]	# Conta do Beneficiário (Sem o digito verificador)
  zero			        = codebar[43:44]	# Zero


  campo_1 = cod_banco + cod_moeda + campo_livre[0:5]
  campo_1 += criaDV(campo_1)

  campo_2 = campo_livre[5:15]
  campo_2 += criaDV(campo_2)

  campo_3 = campo_livre[15:25]
  campo_3 += criaDV(campo_3)

  campo_4 = dig_verif

  campo_5 = fator_venc + valor

  campo_1 = insert_str(campo_1, '.', 5)
  campo_2 = insert_str(campo_2, '.', 5)
  campo_3 = insert_str(campo_3, '.', 5)

  linha_digitavel = campo_1 + ' ' + campo_2 + ' ' + campo_3 + ' ' + campo_4 + ' ' + campo_5


  return linha_digitavel

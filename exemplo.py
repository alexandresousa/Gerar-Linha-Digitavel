import cv2
from pyzbar.pyzbar import decode


def modulo10(num):
    if not isinstance(num, str):
        raise TypeError

    soma = 0
    peso = 2

    for c in reversed(num):
        parcial = int(c) * peso

        if parcial > 9:
            s = str(parcial)
            parcial = int(s[0]) + int(s[1])

        soma += parcial

        if peso == 2:
            peso = 1
        else:
            peso = 2

    resto10 = soma % 10

    if resto10 == 0:
        modulo10 = 0
    else:
        modulo10 = 10 - resto10

    return str(modulo10)


# Se r = 0 trata-se de boleto de cobrança
# Se r = 1 trata-se de arrecadação/recebimento
def modulo11(num, base=9, r=0):
    if not isinstance(num, str):
        raise TypeError

    soma = 0
    fator = 2

    for c in reversed(num):
        soma += int(c) * fator

        if fator == base: fator = 1

        fator += 1

    resto = soma % 11

    if r == 0:
        if resto in [0, 1, 10]: modulo11 = 1
        else: modulo11 = 11 - resto
    elif r == 1:
        if resto in [0, 1]: modulo11 = 0
        elif resto == 10: modulo11 = 1
        else: modulo11 = 11 - resto

    return str(modulo11)

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

def getBarCodeCobranca(codebar):

    cod_banco 		    = codebar[:3]       # Identificação do Banco
    cod_moeda 		    = codebar[3:4]		# Código da Moeda (Real = 9, Outras=0)
    dig_verif		    = codebar[4:5]		# Dígito verificador do Código de Barras
    fator_venc		    = codebar[5:9]		# Fator de Vencimento (Vide Nota)
    valor			    = codebar[9:19]	    # Valor
    campo_livre         = codebar[19:44]    # Campo Livre


    campo_1 = cod_banco + cod_moeda + campo_livre[0:5]
    campo_1 += modulo10(campo_1)

    campo_2 = campo_livre[5:15]
    campo_2 += modulo10(campo_2)

    campo_3 = campo_livre[15:25]
    campo_3 += modulo10(campo_3)

    Valida_D43 = codebar[:4] + codebar[5:]
    DAC = modulo11(Valida_D43, base=9, r=0)
    if DAC == dig_verif:
        campo_4 = dig_verif
    else:
        return "Erro ao validar o DAC do Boleto de cobrança, forneça esse boleto pra equipe técnica analisar."

    campo_5 = fator_venc + valor

    return campo_1 + campo_2 + campo_3 + campo_4 + campo_5

def getBarCodeArrecadacao(codebar):

    identificacao_produto   = codebar[0]        # Identificação do Produto, constante 8
    identificacao_segmento  = codebar[1:2]		# Identificação do Segmento
    identificacao_valor     = codebar[2:3]      # Identificação do valor real ou referência
    dig_verif		        = codebar[3:4]		# Dígito verificador geral (módulo 10 ou 11) 
    valor			        = codebar[4:15]	    # Valor
    identificacao_empresa   = codebar[15:19]    # Identificação da empresa/órgão
    campo_livre             = codebar[19:44]    # Campo Livre


    Valida_D43 = codebar[:3] + codebar[4:]
    DAC = modulo11(Valida_D43, r=1)
    if DAC == dig_verif:
        campo_4 = dig_verif
    else:
        return "Erro ao validar o DAC do Boleto de arrecadação, forneça esse documento pra equipe técnica analisar."


    campo_1 = codebar[:11]
    campo_2 = codebar[11:22]
    campo_3 = codebar[22:33]
    campo_4 = codebar[33:]

    if int(identificacao_valor) in [6, 7]:
        campo_1 += modulo10(campo_1)
        campo_2 += modulo10(campo_2)
        campo_3 += modulo10(campo_3)
        campo_4 += modulo10(campo_4)
    elif int(identificacao_valor) in [8, 9]:
        campo_1 += modulo11(campo_1, r=1)
        campo_2 += modulo11(campo_2, r=1)
        campo_3 += modulo11(campo_3, r=1)
        campo_4 += modulo11(campo_4, r=1)
    else:
        return "O identificador de valor efetivo ou referência é inválido, forneça esse documento pra equipe técnica analisar."

    return campo_1 + campo_2 + campo_3 + campo_4



if __name__ == "__main__":

    image = cv2.imread('./DAMSP.png')

    detectedBarcodes = decode(image)
    if detectedBarcodes:

        barcode = detectedBarcodes[0].data.decode()

        if int(barcode[0]) == 8:
            linha_digitavel = getBarCodeArrecadacao(barcode)
            print(linha_digitavel)
        else:
            linha_digitavel = getBarCodeCobranca(barcode)
            print(linha_digitavel)


    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    image = cv2.imread('./boleto.png')


    detectedBarcodes = decode(image)
    if detectedBarcodes:

        barcode = detectedBarcodes[0].data.decode()

        if int(barcode[0]) == 8:
            linha_digitavel = getBarCodeArrecadacao(barcode)
            print(linha_digitavel)
        else:
            linha_digitavel = getBarCodeCobranca(barcode)
            print(linha_digitavel)


    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # http://www.informarejuridico.com.br/Prodinfo/boletim/2009/rj/iss_rj_51_2009.html
    # https://www.bb.com.br/docs/pub/emp/mpe/dwn/PadraoCodigoBarras.pdf
    # https://www.bb.com.br/docs/pub/emp/empl/dwn/Doc5175Bloqueto.pdf

#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Integrante: Gabriel Franzoni '''
''' Pre-requisitos de uso: Python3 e PyCrypto '''

import sys, os
from time import sleep

# Usado PyCrypto 2.6.1 em Python3 3.5.4
# https://pypi.org/project/pycrypto/
from Crypto.Hash import SHA256

'''
FUNCAO QUE INICIA O CODIGO
Esta funcao ira pegar os dados de entrada do usuario, que sao o nome do video
e o tamanho do bloco que o video sera quebrado (no caso do trabalho, 1024).

Ele ira mandar para a funcao getHash(), que ira computar o seu hash bloco
por bloco do fim ao seu inicio e no final imprime na tela o resultado

OBSERVACAO: Os videos de input precisam estar dentro do diretorio /cases
'''
def launch():
    
    try:
        # Deve ser digitado o video que tera seu hash calculado
        # Nao deve ser digitada a sua extensao, pois o codigo
        # acrescenta sua extensao e diretorio automaticamente
        clear()
        print('Digite o video (sem a extensao .mp4):')
        video = input()+'.mp4'

        # Arquivo do video sera quebrado em blocos de 1024 bytes
        # Para o trabalho, deve ser digitado 1024 como input
        clear()
        print('Digite o tamanho dos blocos que o arquivo sera quebrado (em bytes):')
        block = input()
        
        # Mostra os dados de entrada para o usuario antes de comecar a operacao
        showInputs(video,block)
        video = 'cases/'+video
        
        print('OPERACAO EM ANDAMENTO...')
        hash_h0 = getHash(video,int(block))
        
        clear()
        print('Computacao realizada com sucesso!\n')
        hash_h0_hex = hash_h0.hex()
        print('Video selecionado: ' + video.replace('cases/',''))
        print('Tamanho do Video: ' + str(os.path.getsize(video)))
        print('Hash final gerada em hex: ' + hash_h0_hex)
        
    except:
        clear()
        print('Ocorreu um erro durante a operacao.')
        print('Tente novamente!')
    
    
'''
FUNCAO QUE COMPUTA O HASH
Esta funcao precisa garantir o tamanho do video. Ela usa o path.getsize
para encontrar o tamanho total do video. Ela entao precisa quebrar em 1024
bytes de tamanho, porem, temos uma excecao, que sera o bloco final do video,
que nem sempre sera 1024, logo, faz operacao que encontra esse tamanho e inicia
um loop onde ele so para quando chega no bloco final (h0). Nesta iteracao, usa
operacoes do OS Python que pega os dados localizados no bloco e usa o SHA-256
para realizar uma atualizacao em cima do Hash e segue passando bloco por bloco.

Quando chegar no h0, ele da o digest e retorna o resultado. O resultado precisa
ser convertido em hexadecimal para visualizar corretamente
'''
def getHash(video,block):
    
    # Como vamos percorrer blocos de bytes do arquivo ate seu inicio,
    # precisamos do seu tamanho em bytes
    # https://stackoverflow.com/questions/6591931/getting-file-size-in-python
    video_size = os.path.getsize(video)
    
    # O bloco final NEM SEMPRE sera 1024, logo, precisamos de seu valor tambem
    last_block = video_size % block
    
    h0 = ''
    
    # Abre o arquivo do video
    with open(video,'rb') as v:
        
        # Verifica se o bloco final sera
        # diferente do tamanho padrao dos blocos
        is_last = False
        if last_block > 0:
            is_last = True
        
        # Inicia iteracao, onde so vai parar
        # quando chegar no h0
        last_position = video_size
        while last_position > 0:
            
            # Pega o bloco em bytes e da refresh
            # no tamanho a cada iteracao para
            # garantir condicao especial do ultimo bloco
            size = block
            if is_last:
                size = last_block
                is_last = False
            
            # Precisa utilizar um tipo de ponteiro para pegar as posicoes do
            # arquivo de video
            # https://www.tutorialspoint.com/python/file_seek.htm
            v.seek(last_position - size)
            block_info = v.read(block)
            last_position -= size
            
            # Aqui o SHA-256 entra em acao para atualizar
            # o hash ate chegar no h0 para garantir integridade
            sha256 = SHA256.new()
            sha256.update(block_info)
            if(h0): sha256.update(h0)
            h0 = sha256.digest()
        
        # Fecha arquivo do video    
        v.close()
        
    return h0
    
    

'''
FUNCOES AUXILIARES DE INTERFACE
As funcoes a seguir servem para ajudar a proporcionar
uma interface textual mais agradavel para o usuario
'''    
def showInputs(video,block):
    clear()
    print('Arquivo do video:',video)
    print('Tamanho do bloco:',block,'bytes')
    print()
    print('A operacao vai começar em 3 segundos...')
    sleep(3)
    clear()
    

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

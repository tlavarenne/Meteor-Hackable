import numpy as np
import math
import PIL
from PIL import Image


np.set_printoptions(edgeitems=75,linewidth=np.inf)#(threshold=np.inf)
def differential_decode(bits, mode="S"):
    out = np.zeros_like(bits)
    if mode == "M":
        prev = 0
        for i, b in enumerate(bits):
            out[i] = b ^ prev
            prev = out[i]
    elif mode == "S":
        out[0] = bits[0]
        for i in range(1, len(bits)):
            out[i] = bits[i] ^ bits[i-1]
    else:
        raise ValueError("Mode doit être 'M' ou 'S'")
    return out
def extraction(fichier):  #fichier = viterbi2.bin (binarymeteor2.s ligne 25!!) modifié ou viterbi.bin (binarymeteor.s)
	
	with open(fichier, "rb") as f:
		data_bytes = np.fromfile(f, dtype=np.uint8)
	bits = np.unpackbits(data_bytes)
	#binary=''
	#for i in range(len(bits)):				# on convertit les octets en binaire sur 8 bits
	#	binary+=bin(bits[i])[2:].zfill(8)
	binary = differential_decode(bits, mode="S")
	binary = ''.join(str(b) for b in binary.tolist())
	binary=binary[binary.find("00011010110011111111110000011101")+32:]  #on se place juste après le premier mot de synchro 1acffc1d

	hexa=''
	for i in range(0,len(binary),8):						#conversion binaire en hexa
		hexa+=hex(int(binary[i:i+8], 2))[2:].zfill(2)
	chunk=[]
	for i in range(0,len(hexa)//2048):						#on récupère les infos en enlevant le mot de synchro
		chunk.append(hexa[i*2048:(i+1)*2048-8])


	chunk_dec=np.zeros((len(chunk),1020), dtype=int)		# on crée une matrice vide

	for j in range(len(chunk)):								#qu'on remplit avec les lignes extraites précédemment
		for i in range(0,1020):
			chunk_dec[j,i]=int(chunk[j][2*i:2*i+2],16)






	pn=[0xff, 0x48, 0x0e, 0xc0, 0x9a, 0x0d, 0x70, 0xbc,
		0x8e, 0x2c, 0x93, 0xad, 0xa7, 0xb7, 0x46, 0xce,
		0x5a, 0x97, 0x7d, 0xcc, 0x32, 0xa2, 0xbf, 0x3e,
		0x0a, 0x10, 0xf1, 0x88, 0x94, 0xcd, 0xea, 0xb1,
		0xfe, 0x90, 0x1d, 0x81, 0x34, 0x1a, 0xe1, 0x79,
		0x1c, 0x59, 0x27, 0x5b, 0x4f, 0x6e, 0x8d, 0x9c,
		0xb5, 0x2e, 0xfb, 0x98, 0x65, 0x45, 0x7e, 0x7c,
		0x14, 0x21, 0xe3, 0x11, 0x29, 0x9b, 0xd5, 0x63,
		0xfd, 0x20, 0x3b, 0x02, 0x68, 0x35, 0xc2, 0xf2,
		0x38, 0xb2, 0x4e, 0xb6, 0x9e, 0xdd, 0x1b, 0x39,
		0x6a, 0x5d, 0xf7, 0x30, 0xca, 0x8a, 0xfc, 0xf8,
		0x28, 0x43, 0xc6, 0x22, 0x53, 0x37, 0xaa, 0xc7,
		0xfa, 0x40, 0x76, 0x04, 0xd0, 0x6b, 0x85, 0xe4,
		0x71, 0x64, 0x9d, 0x6d, 0x3d, 0xba, 0x36, 0x72,
		0xd4, 0xbb, 0xee, 0x61, 0x95, 0x15, 0xf9, 0xf0,
		0x50, 0x87, 0x8c, 0x44, 0xa6, 0x6f, 0x55, 0x8f,
		0xf4, 0x80, 0xec, 0x09, 0xa0, 0xd7, 0x0b, 0xc8,
		0xe2, 0xc9, 0x3a, 0xda, 0x7b, 0x74, 0x6c, 0xe5,
		0xa9, 0x77, 0xdc, 0xc3, 0x2a, 0x2b, 0xf3, 0xe0,
		0xa1, 0x0f, 0x18, 0x89, 0x4c, 0xde, 0xab, 0x1f,
		0xe9, 0x01, 0xd8, 0x13, 0x41, 0xae, 0x17, 0x91,
		0xc5, 0x92, 0x75, 0xb4, 0xf6, 0xe8, 0xd9, 0xcb,
		0x52, 0xef, 0xb9, 0x86, 0x54, 0x57, 0xe7, 0xc1,
		0x42, 0x1e, 0x31, 0x12, 0x99, 0xbd, 0x56, 0x3f,
		0xd2, 0x03, 0xb0, 0x26, 0x83, 0x5c, 0x2f, 0x23,
		0x8b, 0x24, 0xeb, 0x69, 0xed, 0xd1, 0xb3, 0x96,
		0xa5, 0xdf, 0x73, 0x0c, 0xa8, 0xaf, 0xcf, 0x82,
		0x84, 0x3c, 0x62, 0x25, 0x33, 0x7a, 0xac, 0x7f,
		0xa4, 0x07, 0x60, 0x4d, 0x06, 0xb8, 0x5e, 0x47,
		0x16, 0x49, 0xd6, 0xd3, 0xdb, 0xa3, 0x67, 0x2d,
		0x4b, 0xbe, 0xe6, 0x19, 0x51, 0x5f, 0x9f, 0x05,
		0x08, 0x78, 0xc4, 0x4a, 0x66, 0xf5, 0x58]


	for i in range(len(chunk)):
		for j in range(1020):
			chunk_dec[i][j] ^= pn[j%255]


	pointeur=[]
	for i in range(len(chunk)):
		if 64<=chunk_dec[i,0]<=70:
			index=chunk_dec[i][8]*256+chunk_dec[i][9]+12-1
			try:
				#if chunk_dec[i,index]==64 or chunk_dec[i,index]==65 or chunk_dec[i,index]==68:
				pointeur.append(chunk_dec[i][8]*256+chunk_dec[i][9]+12)
				print("ligne",i)
				print(chunk_dec[i,index:index+45])
				
				
		
					
			except:
				pass
	return chunk_dec	

#chunk_dec=extraction("viterbi2.bin")
chunk_dec=extraction("sortieViterbi.bin")



def det_len(k):
	index=chunk_dec[k][8]*256+chunk_dec[k][9]+12-1
	jpeg=chunk_dec[k,index+19:]
	print("longueur totale=",len(chunk_dec[k,index+19:]))
	print("octets=",chunk_dec[k,index+19:index+100])
	print("")


	jpeg_bin=''
	for j in range(len(jpeg)):
		jpeg_bin+=str(bin(jpeg[j]))[2:].zfill(8)
	#print(jpeg_bin[:100])

	dc_code=['00','010','011','100','101','110','1110','11110','111110','1111110','11111110','111111110']
	dc_nbr=[0,1,2,3,4,5,6,7,8,9,10,11]


	ac=[0,2,1,3,3,2,4,3,5,5,4,4,0,0,1,125]
	ac_nbr=[1,2,3,0,4,17,5,18,33,49,65,6,19,81,97,7,34,113,20,50,129,145,161,8,35,66,177,193,
	 21,82,209,240,36,51,98,114,130,9,10,22,23,24,25,26,37,38,39,40,41,42,52,53,54,55,
	 56,57,58,67,68,69,70,71,72,73,74,83,84,85,86,87,88,89,90,99,100,101,102,103,104,
	 105,106,115,116,117,118,119,120,121,122,131,132,133,134,135,136,137,138,146,147,
	 148,149,150,151,152,153,154,162,163,164,165,166,167,168,169,170,178,179,180,181,
	 182,183,184,185,186,194,195,196,197,198,199,200,201,202,210,211,212,213,214,215,
	 216,217,218,225,226,227,228,229,230,231,232,233,234,241,242,243,244,245,246,247,
	 248,249,250]
	 
	ac_hex=[]
	for decimal in ac_nbr:
		ac_hex.append(str(hex(decimal)[2:].zfill(2)))
		 

	ac_code=['00','01','100']
	for j in range(3,len(ac)):
		if ac[j]!=0:	
			ac_code.append(str(bin(int(ac_code[len(ac_code)-1],2)+1))[2:]+'0')
		for i in range(ac[j]-1):
			ac_code.append(str(bin(int(ac_code[len(ac_code)-1],2)+1))[2:])


	#print( ac_code)	
	 
	#jpeg_bin='1111101101010010011001101001000011010'

	liste=[[]]
	
	fin=0
	
	while True:
		try:		
			if jpeg_bin[:4]=='1010':
				jpeg_bin=jpeg_bin[4:]
				

			dct=[]
			huff_dc=False
			for mot in dc_code:
				if mot == jpeg_bin[:len(mot)]:
					nbr=dc_nbr[dc_code.index(mot)]
					huff_dc=True
					break
			if huff_dc==False:
				print(huff_dc)
				print("bad hufmann code DC")
			v=jpeg_bin[len(mot):len(mot)+nbr]
			if jpeg_bin[len(mot)+1] == '1':
				val=int(v,2)
			if jpeg_bin[len(mot)+1] == '0':
				val=int(v,2)-(2**nbr-1)


			dct.append(val)
			#print(jpeg_bin[:100])
			jpeg_bin=jpeg_bin[len(mot)+nbr:]
			#print("DC_code=",mot)
			#print("nbr=",nbr)
			#print("valeur=",v, val)
			#print()

			while jpeg_bin[:4]!='1010':
				
				huff_ac=False
				for mot in ac_code:
					if mot == jpeg_bin[:len(mot)]:
						nbr_hex=ac_hex[ac_code.index(mot)]
						huff_ac=True
						break
				if huff_ac==False:
					print("bad hufmann code AC")
				#print(nbr_hex)
				#print(nbr_hex[0])
				#print(nbr_hex[1])
				nbr_zero=int(nbr_hex[0],16)
				nbr=int(nbr_hex[1],16)
				v=jpeg_bin[len(mot):len(mot)+nbr]
		
				if jpeg_bin[len(mot)] == '1':
					val=int(v,2)
				if jpeg_bin[len(mot)] == '0':
					val=int(v,2)-(2**nbr-1)
				if nbr_zero != 0:
					for i in range(nbr_zero):
						val_zero=0
						dct.append(val_zero)
					
					
			
			
				dct.append(val)
				#print(jpeg_bin[:200])
				jpeg_bin=jpeg_bin[len(mot)+nbr:]
				#print("AC_code=",mot)
				#print("nbr=",nbr)
				#print("valeur=",v,' donc:',val)
				#print()
		

			fin+=1	
		
		except:
			break
	return fin

def huff(k,end):
	index=chunk_dec[k][8]*256+chunk_dec[k][9]+12-1
	jpeg=chunk_dec[k,index+19:]
	
	print("octets=",chunk_dec[k,index+19:index+100])
	print("")


	jpeg_bin=''
	for j in range(len(jpeg)):
		jpeg_bin+=str(bin(jpeg[j]))[2:].zfill(8)
	print("nbr total octets compressés=",len(jpeg))

	dc_code=['00','010','011','100','101','110','1110','11110','111110','1111110','11111110','111111110']
	dc_nbr=[0,1,2,3,4,5,6,7,8,9,10,11]


	ac=[0,2,1,3,3,2,4,3,5,5,4,4,0,0,1,125]
	ac_nbr=[1,2,3,0,4,17,5,18,33,49,65,6,19,81,97,7,34,113,20,50,129,145,161,8,35,66,177,193,
	 21,82,209,240,36,51,98,114,130,9,10,22,23,24,25,26,37,38,39,40,41,42,52,53,54,55,
	 56,57,58,67,68,69,70,71,72,73,74,83,84,85,86,87,88,89,90,99,100,101,102,103,104,
	 105,106,115,116,117,118,119,120,121,122,131,132,133,134,135,136,137,138,146,147,
	 148,149,150,151,152,153,154,162,163,164,165,166,167,168,169,170,178,179,180,181,
	 182,183,184,185,186,194,195,196,197,198,199,200,201,202,210,211,212,213,214,215,
	 216,217,218,225,226,227,228,229,230,231,232,233,234,241,242,243,244,245,246,247,
	 248,249,250]
	 
	ac_hex=[]
	for decimal in ac_nbr:
		ac_hex.append(str(hex(decimal)[2:].zfill(2)))
		 

	ac_code=['00','01','100']
	for j in range(3,len(ac)):
		if ac[j]!=0:	
			ac_code.append(str(bin(int(ac_code[len(ac_code)-1],2)+1))[2:]+'0')
		for i in range(ac[j]-1):
			ac_code.append(str(bin(int(ac_code[len(ac_code)-1],2)+1))[2:])


	#print( ac_code)	
	 
	#jpeg_bin='1111101101010010011001101001000011010'

	liste=[[]]
	Q=chunk_dec[k,index+18]
	fin=0
	
	while fin<end:
				
		if jpeg_bin[:4]=='1010':
			jpeg_bin=jpeg_bin[4:]
			

		dct=[]
		huff_dc=False
		for mot in dc_code:
			if mot == jpeg_bin[:len(mot)]:
				nbr=dc_nbr[dc_code.index(mot)]
				huff_dc=True
				break
		if huff_dc==False:
			print(huff_dc)
			print("bad hufmann code DC")
		v=jpeg_bin[len(mot):len(mot)+nbr]
		if jpeg_bin[len(mot)+1] == '1':
			val=int(v,2)
		if jpeg_bin[len(mot)+1] == '0':
			val=int(v,2)-(2**nbr-1)


		dct.append(val)
		#print(jpeg_bin[:100])
		jpeg_bin=jpeg_bin[len(mot)+nbr:]
		#print("DC_code=",mot)
		#print("nbr=",nbr)
		#print("valeur=",v, val)
		#print()

		while jpeg_bin[:4]!='1010':
			
			huff_ac=False
			for mot in ac_code:
				if mot == jpeg_bin[:len(mot)]:
					nbr_hex=ac_hex[ac_code.index(mot)]
					huff_ac=True
					break
			if huff_ac==False:
				print("bad hufmann code AC")
			#print(nbr_hex)
			#print(nbr_hex[0])
			#print(nbr_hex[1])
			nbr_zero=int(nbr_hex[0],16)
			nbr=int(nbr_hex[1],16)
			v=jpeg_bin[len(mot):len(mot)+nbr]
			#try:
			if jpeg_bin[len(mot)] == '1':
				val=int(v,2)
			if jpeg_bin[len(mot)] == '0':
				val=int(v,2)-(2**nbr-1)
			if nbr_zero != 0:
				for i in range(nbr_zero):
					val_zero=0
					dct.append(val_zero)
				
				
		
		
			dct.append(val)
			#print(jpeg_bin[:200])
			jpeg_bin=jpeg_bin[len(mot)+nbr:]
			#print("AC_code=",mot)
			#print("nbr=",nbr)
			#print("valeur=",v,' donc:',val)
			#print()
			#except:
			#	pass


		print("dct=",dct)
		liste.append(dct)
		print(len(liste))
		fin+=1

	
	print()
	print()
	for i in range(1,end):
		liste[i+1][0]=-liste[i+1][0]+ liste[i][0]
	som=0
	for dct in liste:
		som+=len(dct)
		
	print("nbr octets décompressés=",som)


	return liste#,Q,end



def huffman(chaine):
	#index=chunk_dec[k][8]*256+chunk_dec[k][9]+12-1
	#jpeg=chunk_dec[k,index+19:]
	#print("longueur totale=",len(chunk_dec[k,index+19:]))
	#print("octets=",chunk_dec[k,index+19:index+100])
	#print("")


	#jpeg_bin=''
	#for j in range(len(jpeg)):
	#	jpeg_bin+=str(bin(jpeg[j]))[2:].zfill(8)
	#print(jpeg_bin[:100])

	dc_code=['00','010','011','100','101','110','1110','11110','111110','1111110','11111110','111111110']
	dc_nbr=[0,1,2,3,4,5,6,7,8,9,10,11]


	ac=[0,2,1,3,3,2,4,3,5,5,4,4,0,0,1,125]
	ac_nbr=[1,2,3,0,4,17,5,18,33,49,65,6,19,81,97,7,34,113,20,50,129,145,161,8,35,66,177,193,
	 21,82,209,240,36,51,98,114,130,9,10,22,23,24,25,26,37,38,39,40,41,42,52,53,54,55,
	 56,57,58,67,68,69,70,71,72,73,74,83,84,85,86,87,88,89,90,99,100,101,102,103,104,
	 105,106,115,116,117,118,119,120,121,122,131,132,133,134,135,136,137,138,146,147,
	 148,149,150,151,152,153,154,162,163,164,165,166,167,168,169,170,178,179,180,181,
	 182,183,184,185,186,194,195,196,197,198,199,200,201,202,210,211,212,213,214,215,
	 216,217,218,225,226,227,228,229,230,231,232,233,234,241,242,243,244,245,246,247,
	 248,249,250]
	 
	ac_hex=[]
	for decimal in ac_nbr:
		ac_hex.append(str(hex(decimal)[2:].zfill(2)))
		 

	ac_code=['00','01','100']
	for j in range(3,len(ac)):
		if ac[j]!=0:	
			ac_code.append(str(bin(int(ac_code[len(ac_code)-1],2)+1))[2:]+'0')
		for i in range(ac[j]-1):
			ac_code.append(str(bin(int(ac_code[len(ac_code)-1],2)+1))[2:])


	#print( ac_code)	
	 
	jpeg_bin=chaine

	liste=[[]]
	
	fin=0
	end=1
	while fin<end:
				
		if jpeg_bin[:4]=='1010':
			jpeg_bin=jpeg_bin[4:]
			

		dct=[]
		huff_dc=False
		for mot in dc_code:
			if mot == jpeg_bin[:len(mot)]:
				nbr=dc_nbr[dc_code.index(mot)]
				huff_dc=True
				break
		if huff_dc==False:
			print(huff_dc)
			print("bad hufmann code DC")
		v=jpeg_bin[len(mot):len(mot)+nbr]
		if jpeg_bin[len(mot)+1] == '1':
			val=int(v,2)
		if jpeg_bin[len(mot)+1] == '0':
			val=int(v,2)-(2**nbr-1)


		dct.append(val)
		#print(jpeg_bin[:100])
		jpeg_bin=jpeg_bin[len(mot)+nbr:]
		#print("DC_code=",mot)
		#print("nbr=",nbr)
		#print("valeur=",v, val)
		#print()

		while jpeg_bin[:4]!='1010':
			
			huff_ac=False
			for mot in ac_code:
				if mot == jpeg_bin[:len(mot)]:
					nbr_hex=ac_hex[ac_code.index(mot)]
					huff_ac=True
					break
			if huff_ac==False:
				print("bad hufmann code AC")
			#print(nbr_hex)
			#print(nbr_hex[0])
			#print(nbr_hex[1])
			nbr_zero=int(nbr_hex[0],16)
			nbr=int(nbr_hex[1],16)
			v=jpeg_bin[len(mot):len(mot)+nbr]
			#try:
			if jpeg_bin[len(mot)] == '1':
				val=int(v,2)
			if jpeg_bin[len(mot)] == '0':
				val=int(v,2)-(2**nbr-1)
			if nbr_zero != 0:
				for i in range(nbr_zero):
					val_zero=0
					dct.append(val_zero)
				
				
		
		
			dct.append(val)
			#print(jpeg_bin[:200])
			jpeg_bin=jpeg_bin[len(mot)+nbr:]
			#print("AC_code=",mot)
			#print("nbr=",nbr)
			#print("valeur=",v,' donc:',val)
			#print()
			#except:
			#	pass


		print("dct=",dct)
		liste.append(dct)

		fin+=1

	
	print()
	print()
	for i in range(1,end):
		liste[i+1][0]=-liste[i+1][0]+ liste[i][0]


def zigzag(ligne,nbr,x):
	liste=huff(ligne,nbr)
	liste=liste[1:]
	zigzag=[[ 0, 1, 5, 6, 14, 15, 27, 28],
			 [2, 4, 7, 13, 16, 26, 29, 42],
			 [3, 8, 12, 17, 25, 30, 41, 43],
			 [9, 11, 18, 24, 31, 40, 44, 53],
			 [10, 19, 23, 32, 39, 45, 52, 54],
			 [20, 22, 33, 38, 46, 51, 55, 60],
			 [21, 34, 37, 47, 50, 56, 59, 61], 
			 [35, 36, 48, 49, 57, 58, 62, 63]]

	zig=np.array(zigzag)

	
	DCT=np.zeros((8,8), dtype=float)

	liste2=[]
	for i in range(64):
		liste2.append(0)

	for i in range(len(liste[x])):
		liste2[i]=liste[x][i]

	for i in range(8):
		for j in range(8):
			DCT[i,j]=liste2[zig[i,j]]
	return DCT

def quantif(DCT,Q):
	HTK=[
	[16,11,10,16,24,40,51,61],
	[12,12,14,19,26,58,60,55],
	[14,13,16,24,40,57,69,56],
	[14,17,22,29,51,87,80,62],
	[18,22,37,56,68,109,103,77],
	[24,35,55,64,81,104,113,92],
	[49,64,78,87,103,121,120,101],
	[72,92,95,98,112,100,103,99]
	]

	PTK=[
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0]
	]

	if 20<Q<50:			### COMPLÉTER ICI
		F=5000/Q*1.0
	if 50<=Q<=100:
		F=200-2*Q*1.0
		

	for u in range(0,8):
		for v in range(0,8):
			PTK[u][v]=round(HTK[u][v]*F/100.0)
			if PTK[u][v]<1:
				PTK[u][v]=1
	PTK=np.array(PTK)
	print("PTK=",PTK)

	F0=np.zeros((8,8), dtype=float)


	for i in range(8):
		for j in range(8):
			F0[i,j]=DCT[i,j]*PTK[i,j]
		
	print("F0=",F0)
	return F0



def tcdi(F0):	
	S=np.zeros((8,8), dtype=float)
	
	for x in range(0,8):
		for y in range(0,8):
			somme=0
			for u in range(0,8):
				for v in range(0,8):
					if u==0:
						Cu=1/math.sqrt(2)
					if v==0:
						Cv=1/math.sqrt(2)
					if u!=0:
						Cu=1
					if v!=0:
						Cv=1
						
					somme+=0.25*(Cu*Cv*F0[u,v]*math.cos((2*x+1)*u*math.pi/16)*math.cos((2*y+1)*v*math.pi/16))
			
					if somme >127:
						somme=127
					if somme<-128:
						somme=-128
			S[x,y]=round(somme)
	print("S=",S)
	return S


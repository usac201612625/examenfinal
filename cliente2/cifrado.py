from Crypto.Cipher import DES

cipher = DES.new('!#$%aser')

def cifrar(c_msj): 
        g = []
        f = 0
        for i in range(0,len(c_msj),8):
            g.append(c_msj[i:8+i])
            if len(g[f]) <8:
                while len(g[f])<8:
                    g[f]=g[f]+ ' '
            f += 1
        c_usuario = [ ]
        c_msg = b''
        for i in range(len(g)):
            c_usuario.append(cipher.encrypt(g[i]))
            c_msg = c_msg + c_usuario[i]
        return c_msg

def descifrar(d_msj):
    cc_msg=[ ]
    for i in range(0,len(d_msj),8):
        cc_msg.append(d_msj[i:8+i])
    d_usuario = [ ]
    msg = ''
    for i in range(len(cc_msg)):
        d_usuario .append(cipher.decrypt(cc_msg[i]).strip().decode("utf-8") )
        msg = msg + d_usuario[i]
    return msg



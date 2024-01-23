import math

# crear clase que sea rastreador
class Rastreador:
    # --- init variables
    def __init__(self):
        #almacenado de posiciones centrales de los objetos
        self.centro_puntos = {}
        #Contador de objetos
        self.id_count = 0

    def rastreo(self, objetos):
        #almacenar obj identificados
        objetos_id = []

        # Obtener el punto central del nuevo objeto
        for rect in objetos:
            x ,y , w , h = rect
            cx = (x +x +w)//2
            cy = (y +y +h)//2

            # chequear si el obj ya fue detectado antes
            objeto_det = False
            for id , pt in self.centro_puntos.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist < 25:
                    self.centro_puntos[id] = (cx,cy)
                    objetos_id.append([x,y,w,h,id])
                    objeto_det = True
                    break

            #Si detecta un nuevo objeto le asignamos el ID a ese objeto
            if objeto_det is False:
                self.centro_puntos[self.id_count] = (cx , cy) # almacena la cordenada x e y
                objetos_id.append([x,y,w,h,self.id_count])
                self.id_count += 1

        #Limpiar lista por puntos centrales para eliminar IDS que ya no se usan
        new_center_points = {}
        for obj_bb_id in objetos_id:
            _,_,_,object_id = obj_bb_id
            center = self.centro_puntos[object_id]
            new_center_points[object_id] = center




# https://www.youtube.com/watch?v=dRVPONsESqw

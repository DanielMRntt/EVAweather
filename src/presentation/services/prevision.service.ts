
import { PrismaClient } from '@prisma/client';



export class PrevisionService {

async obtenerPrevision(ciudadNombre: string, fecha: Date) {
    const prisma = new PrismaClient();
  const prevision = await prisma.prevision.findFirst({
    where: {
      fecha: fecha,
      ciudad: {
        nombre: ciudadNombre,
      },
    },
    include: {
      ciudad: true,
      condicion_meteorologica: true,
    },
  });

  return prevision;
}

returnResponse(previsiones: any | any[]) {

    const response = {
      option: "OK",
      openContext: {},
      visibleContext: {},
      hiddenContext: {
        previsiones: previsiones.map((prevision: any) => ({
          ciudad: prevision.ciudad.nombre,
          fecha: prevision.fecha.toISOString().split('T')[0],
          condicion: prevision.condicion_meteorologica.detalle,
          temperaturaMax: prevision.temperaturaMaxima,
          temperaturaMin: prevision.temperaturaMinima,
        })),
      }
    };



    return response;
  }

}
   





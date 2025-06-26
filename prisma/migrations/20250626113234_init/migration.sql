-- CreateTable
CREATE TABLE "Ciudad" (
    "id" SERIAL NOT NULL,
    "nombre" TEXT NOT NULL,
    "latitud" DOUBLE PRECISION NOT NULL,
    "longitud" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "Ciudad_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "CondicionMeteorologica" (
    "id" SERIAL NOT NULL,
    "tipo" TEXT NOT NULL,
    "detalle" TEXT NOT NULL,

    CONSTRAINT "CondicionMeteorologica_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Prevision" (
    "id" SERIAL NOT NULL,
    "fecha" TIMESTAMP(3) NOT NULL,
    "temperaturaMinima" DOUBLE PRECISION NOT NULL,
    "temperaturaMaxima" DOUBLE PRECISION NOT NULL,
    "ciudadId" INTEGER NOT NULL,
    "condicionId" INTEGER NOT NULL,

    CONSTRAINT "Prevision_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Prevision_ciudadId_fecha_key" ON "Prevision"("ciudadId", "fecha");

-- AddForeignKey
ALTER TABLE "Prevision" ADD CONSTRAINT "Prevision_ciudadId_fkey" FOREIGN KEY ("ciudadId") REFERENCES "Ciudad"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Prevision" ADD CONSTRAINT "Prevision_condicionId_fkey" FOREIGN KEY ("condicionId") REFERENCES "CondicionMeteorologica"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

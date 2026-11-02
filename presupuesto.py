# Costo por fase de TrazaGrano: costo = semanas x dedicacion x costo semanal del rol
FACTOR_EMPLEADOR = 1.52   # salario + prestaciones + seguridad social + parafiscales
SEMANAS_AL_ANIO = 52

salarios = {             # salario mensual estimado en COP
    "gerente": 7_000_000, "analista_ux": 4_200_000, "backend": 5_800_000,
    "movil": 4_500_000,   "web": 3_600_000,         "qa": 3_000_000,
    "devops": 5_500_000,  "campo": 2_800_000,
}

def costo_semana(rol):
    return salarios[rol] * FACTOR_EMPLEADOR * 12 / SEMANAS_AL_ANIO

# (fase, actividad, semana inicio, semana fin, {rol: dedicacion})
actividades = [
 ("F1 Inicio", "Acta de inicio y plan del proyecto",      1,  2, {"gerente": 1.0}),
 ("F1 Inicio", "Factibilidad y mapa de interesados",      2,  3, {"gerente": .5, "analista_ux": 1.0}),
 ("F2 Análisis y diseño", "Levantar requisitos en campo",  3,  5, {"gerente": .5, "analista_ux": 1.0, "campo": 1.0}),
 ("F2 Análisis y diseño", "Diseño UX y prototipo",         4,  6, {"analista_ux": 1.0, "web": .5}),
 ("F2 Análisis y diseño", "Arquitectura y modelo de datos",5,  6, {"backend": 1.0, "devops": .5}),
 ("F3 Desarrollo", "Sprint 1: base, usuarios y permisos",  7,  8, {"gerente": .5, "backend": 1.0, "movil": 1.0, "web": 1.0, "devops": .5}),
 ("F3 Desarrollo", "Sprint 2: fincas, parcelas y mapa",    9, 10, {"gerente": .5, "backend": 1.0, "movil": 1.0, "web": 1.0, "qa": .5}),
 ("F3 Desarrollo", "Sprint 3: lotes y modo sin internet", 11, 12, {"gerente": .5, "backend": 1.0, "movil": 1.0, "web": 1.0, "qa": .5}),
 ("F3 Desarrollo", "Sprint 4: acopio, QR y documentos",   13, 14, {"gerente": .5, "backend": 1.0, "movil": 1.0, "web": 1.0, "qa": .5}),
 ("F3 Desarrollo", "Sprint 5: paquete para exportador",   15, 16, {"gerente": .5, "backend": 1.0, "movil": 1.0, "web": 1.0, "qa": 1.0}),
 ("F4 Pruebas", "Pruebas integrales y corrección",        17, 18, {"gerente": .5, "backend": 1.0, "movil": 1.0, "web": .5, "qa": 1.0}),
 ("F4 Pruebas", "Prueba de seguridad y de datos",         18, 18, {"devops": 1.0}),
 ("F5 Piloto", "Capacitar técnicos y productores",        19, 20, {"gerente": .5, "analista_ux": 1.0, "campo": 1.0}),
 ("F5 Piloto", "Piloto con 300 caficultores",             19, 22, {"gerente": .5, "backend": .5, "movil": .5, "qa": .5, "campo": 2.0}),
 ("F6 Cierre", "Salida a producción y manuales",          23, 23, {"backend": 1.0, "devops": 1.0, "qa": .5}),
 ("F6 Cierre", "Entrega, lecciones y cierre",             23, 24, {"gerente": 1.0, "analista_ux": .5}),
]

# (rubro, concepto, valor, fase)
otros_costos = [
 ("Hardware", "4 portátiles de desarrollo", 15_200_000, "F1 Inicio"),
 ("Hardware", "6 celulares Android para campo", 5_100_000, "F5 Piloto"),
 ("Hardware", "2 GPS de mano", 3_200_000, "F2 Análisis y diseño"),
 ("Software", "Nube para desarrollo y pruebas", 4_000_000, "F3 Desarrollo"),
 ("Software", "Nube para el piloto", 3_000_000, "F5 Piloto"),
 ("Software", "Licencias de diseño y gestión", 1_800_000, "F2 Análisis y diseño"),
 ("Software", "Mapas sin conexión", 1_200_000, "F3 Desarrollo"),
 ("Software", "Cuenta de Google Play", 100_000, "F6 Cierre"),
 ("Comunicaciones", "Planes de datos, 6 líneas por 5 meses", 1_950_000, "F5 Piloto"),
 ("Comunicaciones", "Internet y videollamadas del equipo", 2_100_000, "F3 Desarrollo"),
 ("Comunicaciones", "Mensajes de aviso a productores", 1_000_000, "F5 Piloto"),
 ("Recursos físicos", "Puestos de coworking por 6 meses", 14_400_000, "F3 Desarrollo"),
 ("Recursos físicos", "Visita de campo para requisitos", 2_500_000, "F2 Análisis y diseño"),
 ("Recursos físicos", "3 visitas de campo en el piloto", 7_500_000, "F5 Piloto"),
 ("Recursos físicos", "2 impresoras y etiquetas QR", 3_000_000, "F5 Piloto"),
 ("Administrativos y legales", "Abogado de datos personales", 6_000_000, "F2 Análisis y diseño"),
 ("Administrativos y legales", "Contador por 6 meses", 3_000_000, "F6 Cierre"),
 ("Administrativos y legales", "Pólizas y contratos", 2_500_000, "F1 Inicio"),
 ("Administrativos y legales", "Prueba de seguridad externa", 7_000_000, "F4 Pruebas"),
 ("Mercadeo", "3 talleres de socialización", 4_500_000, "F5 Piloto"),
 ("Mercadeo", "Piezas y material para productores", 1_500_000, "F5 Piloto"),
]
IMPREVISTOS = 0.10

fases, rubros = {}, {"Recursos humanos": 0}
for fase, _, ini, fin, roles in actividades:
    semanas = fin - ini + 1
    costo = sum(semanas * ded * costo_semana(r) for r, ded in roles.items())
    fases[fase] = fases.get(fase, 0) + costo
    rubros["Recursos humanos"] += costo

for rubro, _, valor, fase in otros_costos:
    fases[fase] = fases.get(fase, 0) + valor
    rubros[rubro] = rubros.get(rubro, 0) + valor

subtotal = sum(rubros.values())
rubros["Imprevistos (10 %)"] = subtotal * IMPREVISTOS
fases = {f: c * (1 + IMPREVISTOS) for f, c in fases.items()}
total = subtotal * (1 + IMPREVISTOS)

if __name__ == "__main__":
    for fase, costo in fases.items():
        print(f"{fase:24} ${costo:>13,.0f}  {costo/total:5.1%}")
    print(f"{'TOTAL':24} ${total:>13,.0f}")

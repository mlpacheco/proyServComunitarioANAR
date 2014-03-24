# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ObjectDoesNotExist
from smart_selects.db_fields import ChainedForeignKey

########################################################################################
# Clases modificadas
########################################################################################

def short_text(text):
	""" Retorna un string limitado para evitar que los toString se vean muy largos"""
	return text[0:100]

class CharField(models.CharField):
	
	"""Tipo de Dato implementado para evitar que los campos títulos y textos se 
	vean limitados, al utilizar el tipo de datos de postgre 'text' que es sin limite."""

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('max_length', 65000)
		super(CharField, self).__init__(*args, **kwargs)

	def db_type(self, connection):
		return 'text'

	def south_field_triple(self):
		"""Only necessary if using South migrations, which you should."""
		from south.modelsinspector import introspector
		field_class = self.__class__.__module__ + "." + self.__class__.__name__
		args, kwargs = introspector(self)
		return (field_class, args, kwargs)
		
########################################################################################
# Diagrama de yacimiento
########################################################################################

class Estado(models.Model):
        
    nombre = CharField('3. Estado/Provincia')
    activo = models.IntegerField('Activo', validators=[MinValueValidator(0), MaxValueValidator(1)])
     
    #representacion en string de un objeto de tipo estado
    def __unicode__(self):
        return self.nombre
        	
    abbr = 'edo'

    class Meta:
        verbose_name = '3. Estado/Provincia'
        verbose_name_plural = '3. Estado/Provincia'

class Municipio(models.Model):
        
    nombre = CharField('2. Municipio')
    estado = models.ForeignKey(Estado, related_name='Municipio')	
    activo = models.IntegerField('Activo', validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    #representacion en string de un objeto de tipo municipio
    def __unicode__(self):
        return self.nombre
        	
    abbr = 'mpio'

    class Meta:
        verbose_name = '2. Municipio'
        verbose_name_plural = '2. Municipios'		
		
class Yacimiento(models.Model):
       
    codigo = models.CharField('(00). Codigo ANAR', unique = True, max_length=20)
    pais = CharField('0. Pais',  default = 'Venezuela')
    nombre = CharField('1. Nombre(s) del Yacimiento')
    estado = models.ForeignKey(Estado, related_name='EstadoYac', blank = True, null = True)		    
    municipio = ChainedForeignKey(Municipio, related_name='MunicipioYac', blank = True, null = True,
					chained_field = 'estado', chained_model_field = 'estado', show_all = False, auto_choose = True)
	     
    #representacion en string de un objeto tipo Yacimiento
    def __unicode__(self):
        return short_text('PB1-' + self.codigo + '-' + self.nombre)
        
    def _get_tipo_manifestaciones(self):
	
        "Determina los tipos de manifestaciones presentes en un yacimiento"
        try :
            manifestacion = ManifestacionYacimiento.objects.get(yacimiento=self.id)
            return manifestacion.texto_descriptivo
        except ObjectDoesNotExist:
            return '';
			
    tipos_de_manifestaciones = property(_get_tipo_manifestaciones, '13. Tipo de Manifestación')
	
    abbr = 'yac'

    class Meta:
        verbose_name = 'Yacimiento'
        verbose_name_plural = 'Yacimientos'



class Yacimiento(models.Model):
       
    codigo = models.CharField('(00). Codigo ANAR', unique = True, max_length=20)
    pais = CharField('0. Pais',  default = 'Venezuela')
    nombre = CharField('1. Nombre(s) del Yacimiento')
    municipio = CharField('2. Municipio')    
    estado = CharField('3. Estado/Provincia')    
     
    #representacion en string de un objeto tipo Yacimiento
    def __unicode__(self):
        return short_text('PB1-' + self.codigo + '-' + self.nombre)
        
    def _get_tipo_manifestaciones(self):
	
        "Determina los tipos de manifestaciones presentes en un yacimiento"
        try :
            manifestacion = ManifestacionYacimiento.objects.get(yacimiento=self.id)
            return manifestacion.texto_descriptivo
        except ObjectDoesNotExist:
            return '';
			
    tipos_de_manifestaciones = property(_get_tipo_manifestaciones, '13. Tipo de Manifestación')
	
    abbr = 'yac'

    class Meta:
        verbose_name = 'Yacimiento'
        verbose_name_plural = 'Yacimientos'

class LocalidadYacimiento(models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='LocalidadYacimiento')
    
    esCentroPoblado = models.BooleanField('4.1. Centro de Poblado')
    esUrbano = models.BooleanField('4.1.1. Urbano')
    esRural = models.BooleanField('4.1.2. Rural')
    esIndigena = models.BooleanField('4.1.3. Indigena')
    nombrePoblado = CharField('4.1.4. Nombre', blank = True)
    esCentroNoPoblado = models.BooleanField('4.2. No Poblado')
    nombreNoPoblado = CharField('4.2.1. Nombre', blank = True)

    abbr = 'loc'

    def __unicode__(self):
        return '' # '# ' + str(self.id)
            
    class Meta:
        verbose_name = '4. Localidad'
        verbose_name_plural = '4. Localidad'
		
class UsoActSuelo(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='UsoActSuelo')
    
    esForestal = models.BooleanField('5.1. Forestal')
    esGanadero = models.BooleanField('5.2. Ganadero')
    esAgriRiesgo = models.BooleanField('5.3. Agricultura de Riesgo')
    esAgriTemp = models.BooleanField('5.4. Agricultura Temporal')
    esSueloUrbano = models.BooleanField('5.5. Urbano')
    esSueloTuristico = models.BooleanField('5.6. Turístico')
    
    abbr = 'uas'

    class Meta:
        verbose_name = '5. Uso Actual Del Suelo'
        verbose_name_plural = '5. Uso Actual Del Suelo'
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class TenenciaDeTierra(models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='TenenciaDeTierra')
   
    esPrivada = models.BooleanField('5.7.1. Privada')
    esComunal = models.BooleanField('5.7.2. Comunal')
    esEjido = models.BooleanField('5.7.3. Ejido')
    esMunicipal = models.BooleanField('5.7.4. Municipal')
    esABRAE = models.BooleanField('5.7.5. ABRAE (Área Bajo Régimen Especial)')
    esTenenciaOtros = CharField('5.7.6. Otros', blank = True)
    
    abbr = 'tdt'
    
    class Meta:
        verbose_name = '5.7 Tenencia de la Tierra'
        verbose_name_plural = '5.7 Tenencia de la Tierra'

    def __unicode__(self):
        return '' # '# ' + str(self.id)

class Indicaciones(models.Model):
 
    yacimiento = models.OneToOneField(Yacimiento, related_name='Indicaciones')
    
    direcciones = CharField('6.0. Indicaciones para llegar al Yacimiento', blank = True) 
    puntoDatum = CharField('6.1. Punto Datum ', blank = True)
    
    abbr = 'ind'
    
    class Meta:
        verbose_name = '6. Indicaciones para llegar al Yac.'
        verbose_name_plural = '6. Indicaciones para llegar al Yac.'

    def __unicode__(self):
        return '' # '# ' + str(self.id)

class Croquis (models.Model):

    yacimiento = models.ForeignKey(Yacimiento, related_name='Croquis')
    archivo = models.ImageField('6.2. Esquema de llegada - Archivo', upload_to='esquema/%Y_%m', null=True, blank=True)
    
    abbr = 'crq'

    class Meta:
        verbose_name = '..'
        verbose_name_plural = ''

    def __unicode__(self):
        return '' # '# ' + str(self.id)

class Plano (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='Plano')
    numeroPlano = CharField('7. Número de plano', blank = True)
    abbr = 'pln'

    class Meta:
        verbose_name = '7. Número de Plano'
        verbose_name_plural = '7. Número de Plano'
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)

 
class Coordenadas (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='Coordenadas')
    
    longitud = CharField('8. Long. O(W)', blank = True)
    latitud = CharField('8. Lat. N', blank = True)
    utmAdicional = CharField('8. Utm Adicional', blank = True)
    
    abbr = 'crd'

    class Meta:
        verbose_name = '8. Coordenadas'
        verbose_name_plural = '8. Coordenadas'

    def __unicode__(self):
        return '' # '# ' + str(self.id)

class Datum (models.Model):
    
    OPCIONES_DATUM = (
        (1, '9.1 WGS 84'),
        (2, '9.2 La Canoa - Provisional Suramérica 1956'),
    ) 
     
    yacimiento = models.OneToOneField(Yacimiento, related_name='Datum')    
    tipoDatum = models.IntegerField('9. Datum GPS',choices = OPCIONES_DATUM, blank = True,null = True)
    
    abbr = 'dtm'

    class Meta:
        verbose_name = '9. Datum GPS'
        verbose_name_plural = '9. Datum GPS'

    def __unicode__(self):
        return '' # '# ' + str(self.id) 

class Altitud (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='Altitud')

    texto = CharField('10.0. Texto', blank = True)   
    altura = CharField('10.1. Altura en mts', blank = True)
    superficie = CharField('10.2. Superficie en m2', blank = True)
    desarrollo = CharField('10.3. Desarrollo', blank = True)
    desnivel = CharField('10.4. Desnivel', blank = True)
    abbr = 'atd'  

    class Meta:
        verbose_name = '10. Altitud'
        verbose_name_plural = '10. Altitud'

    def __unicode__(self):
        return '' # '# ' + str(self.id)

class FotografiaYac (models.Model):
    
    yacimiento = models.ForeignKey(Yacimiento, related_name='FotografiaYac')
       
    esAerea = models.BooleanField('11. Aerea')
    noEsAerea = models.BooleanField('11. No Aerea')
    esSatelital = models.BooleanField('11. Satelital')
    fecha = models.DateField('11. Fecha',blank = True, null= True)
    archivo = models.ImageField('11. Fotografía - Archivo', upload_to='yacimiento/%Y_%m', null=True, blank=True)
    
    abbr = 'fty'  

    class Meta:
        verbose_name = '11. Fotografia'
        verbose_name_plural = '11. Fotografias'

    def __unicode__(self):
        return '' # '# ' + str(self.id)

class TipoYacimiento (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='TipoYacimiento')

    esParedRocosa = models.BooleanField('12.1. Pared Rocosa')
    esRoca = models.BooleanField('12.2. Roca')
    esDolmen = models.BooleanField('12.3. Dolmen(natural)')
    esAbrigo = models.BooleanField('12.4. Abrigo')
    esCueva = models.BooleanField('12.5. Cueva')
    esCuevadeRec = models.BooleanField('12.6. Cueva de Recubrimiento')
    esTerrenoSup = models.BooleanField('12.7. Terreno Superficial')
    esTerrenoPro = models.BooleanField('12.8. Terreno Profundo')
    
    abbr = 'tyc'

    class Meta:
        verbose_name = '12. Tipo de Yacimiento'
        verbose_name_plural = '12. Tipo de Yacimiento'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)


class ManifestacionYacimiento(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionYacimiento')

    esGeoglifo = models.BooleanField('13.1. Geoglifo')
    esPintura = models.BooleanField('13.2. Pintura Rupestre')
    esPetroglifo = models.BooleanField('13.3. Petroglifo')
    esPetroglifoPintado = models.BooleanField('13.3.1. Petroglifo Pintado')
    esMicroPetroglifo = models.BooleanField('13.4. Micro-Petroglifo')
    esPiedraMiticaNatural = models.BooleanField('13.5. Piedra Mítica Natural')
    esCerroMiticoNatural = models.BooleanField('13.6. Cerro Mítico Natural')
    esCerroConPetroglifo = models.BooleanField('13.6.1. Con Petroglifo')
    esCerroConPintura = models.BooleanField('13.6.2. Con Pintura')
    esCerroConDolmen = models.BooleanField('13.6.3. Con Dolmen')
    esMonumentosMegaliticos = models.BooleanField('13.7. Monumentos Megalíticos')
    esMonolitos = models.BooleanField('13.7.1. Monolitos')
    esMonolitoConGrabados = models.BooleanField('13.7.1.1. Con Grabados')
    esMenhires = models.BooleanField('13.7.2. Menhires')
    esMenhiresConPuntos = models.BooleanField('13.7.2.1. Con Puntos Acoplados')
    esMenhiresConPetroglifo = models.BooleanField('13.7.2.2. Con Petroglifo')
    esMenhiresConPintura = models.BooleanField('13.7.2.3. Con Pintura')
    esAmolador = models.BooleanField('13.8. Amolador')
    esBatea = models.BooleanField('13.9. Batea')
    esPuntosAcoplados = models.BooleanField('13.10. Puntos Acoplados')
    esCupulas = models.BooleanField('13.11. Cupulas')
    esMortero = models.BooleanField('13.12. Mortero o Metate')
	
    abbr = 'tmy'

    def __unicode__(self):
        return '' # '# ' + str(self.id)
	
    def get_texto_descriptivo(self):
	
		"Genera un texto descriptivo de los tipos de manfestacion que representa el objeto"				
		return  (
			('Geoglifo, ' if self.esGeoglifo else '') +
			('Pintura Rupestre, ' if self.esPintura else '') +
			('Petroglifo, ' if self.esPetroglifo else '' ) +
			('Petroglifo Pintado, ' if self.esPetroglifoPintado else '' ) +
			('Micro-Petroglifo, ' if self.esMicroPetroglifo else '' ) +
			('Piedra Mítica Natural, ' if self.esPiedraMiticaNatural else '' ) +
			('Cerro Mítico Natural, ' if self.esCerroMiticoNatural else '' ) + 
			('Cerro Mítico Natural Con Petroglifo, ' if self.esCerroConPetroglifo else '' ) +
			('Cerro Mítico Natural Con Pintura, ' if self.esCerroConPintura else '' ) +
			('Cerro Mítico Natural Con Dolmen, ' if self.esCerroConDolmen else '' ) +
			('Monumentos Megalíticos, ' if self.esMonumentosMegaliticos else '' ) +
			('Monolitos, ' if self.esMonolitos else '' ) +
			('Monolitos Con Grabados, ' if self.esMonolitoConGrabados else '' ) +
			('Menhires, ' if self.esMenhires else '' ) +
			('Menhires Con Puntos Acoplados, ' if self.esMenhiresConPuntos else '' ) +
			('Menhires Con Petroglifo, ' if self.esMenhiresConPetroglifo else '' ) + 
			('Menhires Con Pintura, ' if self.esMenhiresConPintura else '' ) + 
			('Amolador, ' if self.esAmolador else '' ) +
			('Batea, ' if self.esBatea else '' ) +	
			('Puntos Acoplados, ' if self.esPuntosAcoplados else '' ) +
			('Cúpulas, ' if self.esCupulas else '' ) +
			('Mortero o Metate ' if self.esMortero else '') 				
		)
	
    texto_descriptivo = property(get_texto_descriptivo)
	
    class Meta:
        verbose_name = '13. Tipo de Manifestación'
        verbose_name_plural = '13. Tipo de Manifestación'
	
    
class UbicacionYacimiento(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='UbicacionYacimiento')
    
    enCerro = models.BooleanField('14.1. Cerro')
    enCerroCima = models.BooleanField('14.1.1. Cima')
    enCerroLadera = models.BooleanField('14.1.2. Ladera')
    enCerroFalda = models.BooleanField('14.1.3. Falda')
    enCerroFila = models.BooleanField('14.1.4. Fila')
    enCerroPieDeMonte = models.BooleanField('14.1.5. Pie de Monte')
    enCerroBarranco = models.BooleanField('14.1.6. Barranco')
    enCerroAcantilado = models.BooleanField('14.1.7. Acantilado')
    enValle = models.BooleanField('14.2. Valle')
    enRio = models.BooleanField('14.3. Río')
    enRioLecho = models.BooleanField('14.3.1. Lecho')
    enRioMargenDerecha = models.BooleanField('14.3.2. Margen Derecha')
    enRioMargenIzquierda = models.BooleanField('14.3.3. Margen Izquierda')
    enRioIsla = models.BooleanField('14.3.4. Isla')
    enRioRaudal = models.BooleanField('14.3.5. Raudal')
    enRioCosta = models.BooleanField('14.4. Costa')

    abbr = 'ubm'
        
    class Meta:
        verbose_name = '14. Ubicación'
        verbose_name_plural = '14. Ubicación'
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class OrientacionYacimiento (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='OrientacionYacimiento')

    haciaCerro = models.BooleanField('15.1. Hacia Cerro')
    haciaValle = models.BooleanField('15.2. Hacia Valle')
    haciaRio = models.BooleanField('15.3. Hacia Rio')
    haciaCosta = models.BooleanField('15.4. Hacia Costa')
    haciaCielo = models.BooleanField('15.5. Hacia Cielo')
    otros = CharField('15.6. Otros', blank = True)
    orientacion = CharField('15.7. Orientacion Cardinal', blank = True)
    
    abbr = 'oyc'

    class Meta:
        verbose_name = '15. Orientacion del Yacimiento'
        verbose_name_plural = '15. Orientacion del Yacimiento'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class TexturaSuelo (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='TexturaSuelo')

    esRocaMadre = models.BooleanField('16.1. Roca Madre')
    esPedregoso = models.BooleanField('16.2. Pedregoso')
    esArenoso = models.BooleanField('16.3. Arenoso')
    esArcilloso = models.BooleanField('16.4. Arcilloso')
    mixto = CharField('16.5. Mixto', blank = True)
    
    abbr = 'tsl'

    class Meta:
        verbose_name = '16. Textura del Suelo'
        verbose_name_plural = '16. Textura del Suelo'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class FloraYacimiento (models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='FloraYacimiento')    
    flora = CharField('17. Flora', blank = True)
    
    abbr = 'fly'

    class Meta:
        verbose_name = '17. Flora'
        verbose_name_plural = '17. Flora'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class FaunaYacimiento (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='FaunaYacimiento')
    fauna = CharField('18. Fauna', blank = True)
    
    abbr = 'fay'
    
    class Meta:
        verbose_name = '18. Fauna'
        verbose_name_plural = '18. Fauna'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class HidrologiaYacimiento (models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='HidrologiaYacimiento')
    
    rio = models.BooleanField('19.1. Rio')
    laguna = models.BooleanField('19.2. Laguna')
    arroyo = models.BooleanField('19.3. Arroyo')
    arroyoPerenne= models.BooleanField('19.3.1. Perenne')
    manantial = models.BooleanField('19.4. Manantial')
    manantialIntermitente = models.BooleanField('19.4.1. Intermitente')
    otros = CharField('19.5. Otros', blank = True)
    nombre = CharField('19.6. Nombre', blank = True)
    distancia = CharField('19.7. Distancia al Yacimiento', blank = True)
    observaciones = CharField('19.8. Observaciones', blank = True)
    
    abbr = 'hiy'

    class Meta:
        verbose_name = '19. Hidrología'
        verbose_name_plural = '19. Hidrología'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class TipoExposicionYac(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='TipoExposicionYac')
    
    expuesto = models.BooleanField('20.1. Expuesto')
    noExpuesto = models.BooleanField('20.2. No Expuesto')
    expuestoPeriodicamente = models.BooleanField('20.3. Expuesto Periódicamente')
    observaciones = CharField('20.4. Observaciones', blank = True)
    
    abbr = 'tey'

    class Meta:
        verbose_name = '20. Exposición'
        verbose_name_plural = '20. Exposición'

    def __unicode__(self):
        return '' # '# ' + str(self.id)

class ConstitucionYacimiento (models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ConstitucionYacimiento')
    
    nroPiedras = models.IntegerField('21.1. Nro de Piedras en el Yacimiento Original', blank = True, null = True, )
    nroPiedrasGrabadas = models.IntegerField('21.1.1. Nro de Piedras Grabadas', blank = True, null = True, )
    nroPiedrasPintadas = models.IntegerField('21.1.2. Nro de Piedras Pintadas', blank = True, null = True, )
    nroPiedrasColocadas = models.IntegerField('21.1.3. Nro Piedras Colocadas', blank = True, null = True, )
    otros = CharField('21.2. Otros', blank = True)
    
    abbr = 'cny'

    class Meta:
        verbose_name = '21. Constitución del Yacimiento'
        verbose_name_plural = '21. Constitución del Yacimiento'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class MaterialYacimiento(models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='MaterialYacimiento')
        
    esRoca = models.BooleanField('22.1. Roca')
    esIgnea = models.BooleanField('22.1.1. Origen - Ignea')
    esMetamor= models.BooleanField('22.1.2. Origen - Metamórfica')
    esSedimentaria = models.BooleanField('22.1.3. Origen - Sedimentaria')
    tipo = CharField('22.1.4. Origen - Tipo', blank = True)
    esTierra = models.BooleanField('22.2. Tierra')
    esHueso = models.BooleanField('22.3. Hueso')
    esCorteza = models.BooleanField('22.4. Corteza de árbol')
    esPiel = models.BooleanField('22.5. Pieles')
    otros = CharField('22.6. Otros', blank = True)
    
    abbr = 'may'

    class Meta:
        verbose_name = '22. Material'
        verbose_name_plural = '22. Material'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id) 

class TecnicaParaGeoglifo (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='TecnicaParaGeoglifo')
    tecnicas = CharField('23.1. Técnicas de Construcción', blank = True)
    
    abbr = 'tge'
    
    class Meta:
        verbose_name = '13.1. Geoglifo'
        verbose_name_plural = '23. Técnicas'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class TecnicaParaPintura (models.Model):
 
    yacimiento = models.OneToOneField(Yacimiento, related_name='TecnicaParaPintura')
       
    conDedo = models.BooleanField('23.2. Dedo')
    fibra = models.BooleanField('23.3. Fibra')
    soplado = models.BooleanField('23.4. Soplado')
    otros = CharField('23.5. Otros', blank = True)
    
    abbr = 'tpi'

    class Meta:
        verbose_name = '13.2. Pintura Rupestre'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)    

class TecnicaParaPetroglifo (models.Model):
 
    yacimiento = models.OneToOneField(Yacimiento, related_name='TecnicaParaPetroglifo')
       
    esGrabado = models.BooleanField('23.6. Grabado')
    esGrabadoPercusion = models.BooleanField('23.6.1. Percusión')
    esGrabadoPercusionDirecta = models.BooleanField('23.6.1.1. Directa')
    esGrabadoPercusionIndirecta = models.BooleanField('23.6.1.2. Indirecta')
    esAbrasion = models.BooleanField('23.6.2. Abrasión')
    esAbrasionPiedra = models.BooleanField('23.6.2.1. Piedra')
    esAbrasionArena = models.BooleanField('23.6.2.2. Arena')
    esConcha = models.BooleanField('23.6.2.3. Concha')
    otros = CharField('23.6.3. Otros', blank = True)
    
    abbr = 'tpe'

    class Meta:
        verbose_name = '13.3. Petroglifo'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class TecnicaParaMicroPetro (models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='TecnicaParaMicroPetro')
        
    esGrabado = models.BooleanField('23.6. Grabado')
    esGrabadoPercusion = models.BooleanField('23.6.1. Percusión')
    esGrabadoPercusionDirecta = models.BooleanField('23.6.1.1. Directa')
    esGrabadoPercusionIndirecta = models.BooleanField('23.6.1.2. Indirecta')
    esAbrasion = models.BooleanField('23.6.2. Abrasión')
    esAbrasionPiedra = models.BooleanField('23.6.2.1. Piedra')
    esAbrasionArena = models.BooleanField('23.6.2.2. Arena')
    esConcha = models.BooleanField('23.6.2.3. Concha')
    otros = CharField('23.6.3. Otros', blank = True)
    
    abbr = 'tmi'

    class Meta:
        verbose_name = '13.4. Micro-Petroglifo'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class TecnicaParaMonumentos (models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='TecnicaParaMonumentos')
    
    esMonolito = models.BooleanField('13.7.1 Monolitos')
    esMenhir = models.BooleanField('13.7.2 Menhires')
    esDolmen = models.BooleanField('13.7.3 Dolmen (artificial)')
    tecnicas = CharField('23.7. Técnicas de Construcción', blank = True)
    otros = CharField('23.8. Otros', blank = True)
    
    abbr = 'tmo'

    class Meta:
        verbose_name = '13.7. Monumentos Megalíticos'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CaracSurcoPetroglifo (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracSurcoPetroglifo')
    
    anchoDe = CharField('24.1. Ancho desde (en cm)', blank = True)
    anchoA = CharField('24.1. Ancho hasta (en cm)', blank = True)
    produndidadDe = CharField('24.2. Profundidad desde (en cm)', blank = True)
    profundidadA = CharField('24.2. Profundidad hasta (en cm)', blank = True)
    esBase = models.BooleanField('24.3. Base')
    esBaseRedonda = models.BooleanField('24.3.1. Redonda')
    esBaseAguda = models.BooleanField('24.3.2. Aguda')
    esBajoRelieve = models.BooleanField('24.4. Bajo Relieve')
    esBajoRelieveLineal = models.BooleanField('24.5.1. Lineal')
    esBajoRelievePlanar = models.BooleanField('24.5.2. Planar')
    esAltoRelieve = models.BooleanField('24.4.1. Alto Relieve')
    esAltoRelieveLineal = models.BooleanField('24.4.1. Lineal')
    esAltoRelievePlanar = models.BooleanField('24.4.2. Planar')
    esAreaInterlineal = models.BooleanField('24.6. Áreas Interlineales')
    esAreaInterlinealPulida = models.BooleanField('24.6.1. Pulidas')
    esAreaInterlinealRebajada = models.BooleanField('24.6.2. Rebajadas')
    esGrabadoSuperpuesto = models.BooleanField('24.7. Grabados Superpuestos')
    esGrabadoRebajado = models.BooleanField('24.8. Grabados Rebajados')
    
    abbr = 'cpe'

    class Meta:
        verbose_name = '13.3. Petroglifo'
        verbose_name_plural = '24. Características del surco grabado'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CaracSurcoAmoladores(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracSurcoAmoladores')
        
    largo = CharField('24.9. Largo (en cm)', blank = True)
    ancho = CharField('24.10. Ancho (en cm)', blank = True)
    diametro = CharField('24.11. Diámetro (en cm)', blank = True)
    
    abbr = 'cam'

    class Meta:
        verbose_name = '13.9. Amoladores'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)
        
class CaracSurcoBateas(models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracSurcoBateas')
    
    largo = CharField('24.12. Largo (en cm)', blank = True)
    ancho = CharField('24.13. Ancho (en cm)', blank = True)
    diametro = CharField('24.13a. Diametro (en cm)',  blank = True)
    profundidad = CharField('24.13b. Profundidad (en cm)',  blank = True)
    abbr = 'cba'

    class Meta:
        verbose_name = '13.10. Bateas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)


class CaracSurcoPuntosAcopl (models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracSurcoPuntosAcopl')
    esPunteado= models.BooleanField('24.14. Punteado')
    diametro = CharField('24.14a. Diametro (en cm)',  blank = True)
    profundidad = CharField('24.14b. Profundidad (en cm)',  blank = True)
    otros = CharField('24.14c. Otros',  blank = True)    
    
    abbr = 'cpa'
    
    class Meta:
        verbose_name = '13.11. Puntos Acoplados'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CaracSurcoCupulas (models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracSurcoCupulas')
    largo = CharField('24.15. Largo (en cm)', blank = True)
    ancho = CharField('24.16. Ancho (en cm)', blank = True)
    diametro = CharField('24.17. Diámetro (en cm)', blank = True)
    profundidad = CharField('24.17a. Profundidad (en cm)',  blank = True)
    otros = CharField('24.17b. Otros',  blank = True)
    
    abbr = 'ccu'

    class Meta:
        verbose_name = '13.12. Cúpula'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CaracSurcoMortero (models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracSurcoMortero')
    
    largo = CharField('24.9. Largo (en cm)', blank = True)
    ancho = CharField('24.10. Ancho (en cm)', blank = True)
    
    abbr = 'cmr'

    class Meta:
        verbose_name = '13.13. Mortero o Metate'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)


class CaracDeLaPintura (models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracDeLaPintura')

    esPinturaRupestre = models.BooleanField('13.2. Pintura Rupestre')
    esTecnicaDactilar = models.BooleanField('25.1.1. Técnica - Dactilar')
    esTecnicaFibra = models.BooleanField('25.1.2. Técnica - Fibra')
    otros = CharField('25.1.3. Técnica - Otros', blank = True)
    esLineaSencilla= models.BooleanField('25.2.1 Tipo de Línea - Sencilla')
    anchoDe = CharField('25.2.1.1 Ancho desde (en cm)', blank = True)
    anchoA = CharField('25.2.1.2 Ancho hasta (en cm)', blank = True)
    esLineaCompuesta= models.BooleanField('25.2.2 Tipo de Línea - Compuesta')
    anchoDeComp = CharField('25.2.2.1 Ancho desde (en cm)', blank = True)
    anchoAComp = CharField('25.2.2.2 Ancho hasta (en cm)', blank = True)  
    esFiguraRellena = models.BooleanField('25.3. Figura Rellena')
    esImpresionDeManos = models.BooleanField('25.4. Impresión de Manos')
    esImpresionDeManosPositivo = models.BooleanField('25.4.1. Positivo')
    esImpresionDeManosNegativo = models.BooleanField('25.4.2. Negativo')
    tienesFigurasSuperpuestas = models.BooleanField('25.5. Figuras Superpuestas')

    ###IMPORTANTE FALTA 25.6 COLORES ------ PREGUNTAR A RUBY .... 25.6.2 y 25.6.1
    
    abbr = 'pin'
    
    class Meta:
        verbose_name = '13.2. Pintura Rupestre'
        verbose_name_plural = '25. Características de la Pintura'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CaracMonolitos(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracMonolitos')
    
    cantidad = models.IntegerField('26.1. Cantidad ', blank = True, null = True, )
    esPinturaRupestre = models.BooleanField('13.7.1.1 Con Grabados')
    cantidadConGrabados = models.IntegerField('26.2. Cantidad con Grabados', blank = True, null = True, )
    
    abbr = 'mon'

    class Meta:
        verbose_name = '13.7.1. Monolitos'
        verbose_name_plural = '26. Caract. Monumentos Megalíticos'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CaracMenhires(models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracMehnires')
    
    sonPiedrasVerticales = models.BooleanField('26.0. Piedras Verticales')
    cantidadPiedrasVerticales = models.IntegerField('26.3. Cantidad', blank = True, null = True, )
    conPuntosAcoplados = models.BooleanField('13.7.2.1 Con Puntos Acoplados')
    cantidadConPuntosAcoplados = models.IntegerField('26.4. Cantidad', blank = True, null = True, )
    ConPetroglifo = models.BooleanField('13.7.2.2 Con Petroglifo')
    cantidadConPetroglifo = models.IntegerField('26.5. Cantidad', blank = True, null = True, )
    conPinturas = models.BooleanField('13.7.2.3 Con Pinturas')
    cantidadConPinturas = models.IntegerField('26.6. Cantidad', blank = True, null = True, )
    distanciamiento = models.IntegerField('26.7. Distanciamiento (en cm)', blank = True, null = True, )
    
    abbr = 'men'

    class Meta:
        verbose_name = '13.7.2. Menhires'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CaracDolmenArt(models.Model):
   
    yacimiento = models.OneToOneField(Yacimiento, related_name='CaracDolmenArt')
    
    ConPetroglifo = models.BooleanField('13.7.3.1. Con Petroglifo')
    cantidadConPetroglifo = models.IntegerField('26.8. Cantidad', blank = True, null = True, )
    conPinturas = models.BooleanField('13.7.3.2. Con Pinturas')
    cantidadConPinturas = models.IntegerField('26.9. Cantidad', blank = True, null = True, )
    
    abbr = 'dol'

    class Meta:
        verbose_name = '13.7.3. Dolmen'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class NotasYacimiento(models.Model) :

    yacimiento = models.OneToOneField(Yacimiento, related_name='NotasYacimiento')
    notas = CharField('26.10. Notas', blank = True)

    abbr = 'dol'

    class Meta:
        verbose_name = '26.10 Notas'
        verbose_name_plural = '26.10 Notas'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)


class EstadoConserYac(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='EstadoConserYac')
   
    enBuenEstado = models.BooleanField('27.1. Bueno')
    estadoModificado = models.BooleanField('27.2. Modificado')
    trasladado = models.IntegerField('27.2.1. Trasladado', blank = True, null = True,
                                    validators=[MinValueValidator(1), MaxValueValidator(2)] )
    trasladadoPa = CharField('27.2.1. Trasladado Pa(s) Nro ', blank = True)
    sumergido = models.IntegerField('27.2.2. Sumergido', blank = True, null = True,
                                    validators=[MinValueValidator(1), MaxValueValidator(2)] )
    sumergidoPa = CharField('27.2.2. Sumergido Pa(s) Nro ', blank = True)
    enterrado = models.IntegerField('27.2.3. Enterrado', blank = True, null = True,
                                    validators=[MinValueValidator(1), MaxValueValidator(2)] )
    enterradoPa = CharField('27.2.3. Enterrado Pa(s) Nro ', blank = True)
    perdido = models.IntegerField('27.2.4. Perdido', blank = True, null = True,
                                    validators=[MinValueValidator(1), MaxValueValidator(2)] )
    perdidoPa = CharField('27.2.4. Perdido Pa(s) Nro ', blank = True)
    destruido = models.IntegerField('27.2.5. Destruido', blank = True, null = True,
                                     validators=[MinValueValidator(1), MaxValueValidator(2)] )
    destruidoPa = CharField('27.2.5. Destruido Pa(s) Nro ', blank = True)
    crecimientoVeg = models.IntegerField('27.2.6. Crecimiento Vegetal', blank = True, null = True,
                                        validators=[MinValueValidator(1), MaxValueValidator(2)] )
    crecimientoVegPa = CharField('27.2.6. Crecimiento Vegetal Pa(s) Nro ', blank = True)
    patina = models.IntegerField('27.2.7. Pátina', blank = True, null = True,
                                    validators=[MinValueValidator(1), MaxValueValidator(2)] )
    patinaPa = CharField('27.2.7. Pátina Pa(s) Nro ', blank = True)
    erosion = models.IntegerField('27.2.8. Erosión ', blank = True, null = True,
                                     validators=[MinValueValidator(1), MaxValueValidator(2)] )
    erosionPa = CharField('27.2.8. Erosión Pa(s) Nro ', blank = True)
    
    estaDestruido = models.BooleanField('27.3. Grado de Destrucción del Sitio')
    esPorCausaNatural = models.BooleanField('27.3.1. Natural')
    enPorCausaNaturalLigera = models.BooleanField('27.3.1.1. Ligera')
    enPorCausaNaturalAguda = models.BooleanField('27.3.1.2. Aguda')
    enPorCausaHumana = models.BooleanField('27.3.2. Humana')
    enPorCausaHumanaLigera = models.BooleanField('27.3.2.1. Ligera')
    enPorCausaHumanaAguda = models.BooleanField('27.3.2.1. Aguda')
    especificar = CharField('27.4. Especificar Causa y Efecto', blank = True)
    destruccionPotencial = models.BooleanField('27.5. Destrucción Potencial del Sitio')
    
    abbr = 'ecy'

    class Meta:
        verbose_name = '27. Estado de la Conservación'
        verbose_name_plural = '27. Estado de la Conservación'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CausasDestruccionYac(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='CausasDestruccionYac')
	
    porAsentamientoHumand = models.BooleanField('27.5.1.1 Asentamiento Humano')
    porObraCortoPlazo = models.BooleanField('27.5.1.2 Obra Infraestructura a Corto Plazo')
    porObraMedianoPlazo = models.BooleanField('27.5.1.3 Obra Infraestructura a Mediano Plazo')
    porObraLargoPlazo = models.BooleanField('27.5.1.4 Obra Infraestructura a Largo Plazo')
    porNivelacion = models.BooleanField('27.5.1.5 Nivelación del Terreno Como Obra Agrícola')
    porExtraccionFamiliar = models.BooleanField('27.5.1.6 Extracción Como Actividad Familiar')
    porExtraccionMayor = models.BooleanField('27.5.1.7 Extracción Como Actividad Mayor')
    porVandalismo = models.BooleanField('27.5.1.8 Vandalismo')
    porErosion = models.BooleanField('27.5.1.9 Erosión')
    porErosionParModerada = models.BooleanField('27.5.1.9.1 Erosión Parcial Moderada')
    porErosionParSevera = models.BooleanField('27.5.1.9.2 Erosión Parcial Severa')
    porErosionExtModerada = models.BooleanField('27.5.1.9.3 Erosión Extensiva Moderada')
    porErosionExtSevera = models.BooleanField('27.5.1.9.4 Erosión Extensiva Severa')
    otros = CharField('27.5.1.10  Otros', blank = True)
	
    abbr = 'cdy'

    class Meta:
        verbose_name = '27.5.1. Causas'
        verbose_name_plural = '27.5.1. Causas'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class IntensidadDestruccionYac(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='IntensidadDestruccionYac')
    observaciones = CharField('27.6. Observaciones Sobre Intensidad de Destrucción del Sitio, y Otros Procesos No Descritos', blank = True)	
    esDeTiempo = models.BooleanField('27.6.1. Tiempo')
    esInmediato = models.BooleanField('27.6.1.1. Inmediato')
    unAno = models.BooleanField('27.6.1.2. Un Año')
    dosAno = models.BooleanField('27.6.1.3.  Dos Años')
    tresAno = models.BooleanField('27.6.1.4. Tres Años')
    cuatroAno = models.BooleanField('27.6.1.5. Cuatro Años')
    cincoAno = models.BooleanField('27.6.1.6. Cinco Años')
    mas = CharField('27.6.1.7. Más', blank = True)
	
    abbr = 'idy'

    class Meta:
        verbose_name = '27.6.1. Tiempo'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)
	
class ConsiderTemp(models.Model):
    
    yacimiento = models.OneToOneField(Yacimiento, related_name='ConsiderTemp')
    
    cincoAno = models.BooleanField('28.1. Patina')
    otros = CharField('28.2. Otros', blank = True)
    
    abbr = 'tem'
        
    class Meta:
        verbose_name = '28. Consider. sobre Temporalidad'
        verbose_name_plural = '28. Consider. sobre Temporalidad'
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class CronologiaTentativa(models.Model):
    
    yacimiento = models.ForeignKey(Yacimiento, related_name='CronologiaTentativa')
    
    esCrono1 = models.BooleanField('29.1. Anterior a 5000 a.p.')
    esCrono2 = models.BooleanField('29.2. 5000 - 1500 a.p.')
    esCrono3 = models.BooleanField('29.3. 1500 a.p. - 200 n.e.')
    esCrono4 = models.BooleanField('29.4. 200 - 650/900 n.e.')
    esCrono5 = models.BooleanField('29.5. 650/900 - 1200 n.e.')
    esCrono6 = models.BooleanField('29.6. 1200 - 1521 n.e.')
    esCrono7 = models.BooleanField('29.7. Post 1521 n.e.')
    autor = CharField('29.8.  Autor', blank = True)
    fecha = CharField('29.8.1. Fecha', blank = True)
    institucion = CharField('29.8.2. Institución', blank = True)
    pais = CharField('29.8.3. País', blank = True)
    direccion = CharField('29.8.4. Dirección', blank = True)
    telefono = CharField('29.8.5. Tel/Fax', blank = True)
    mail = CharField('29.8.6. Correo Electrónico', blank = True)
    tecnica = CharField('29.8.7. Técnica', blank = True)
    bibliografia = CharField('29.8.8. Bibliografía', blank = True)
    twitter = CharField('29.8.9. Twitter', blank = True)
    facebook = CharField('29.8.10. Facebook', blank = True)

    abbr = 'cte'
    
    class Meta:
        verbose_name = '29. Cronología Tentativa'
        verbose_name_plural = '29. Cronología Tentativa'
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)
	
class ManifestacionesAsociadas(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesAsociadas')
	 
    esLitica = models.BooleanField('30.1. Lítica')
    descripcionLitica = CharField('30.1. Descripción Lítica', blank = True)
    esCeramica = models.BooleanField('30.2. Cerámica')
    descripcionCeramica = CharField('30.2. Descripción Cerámica', blank = True)
    esOseo = models.BooleanField('30.3. Oseo')
    descripcionOseo = CharField('30.3. Descripción Oseo', blank = True)
    esConcha = models.BooleanField('30.4. Concha')
    descripcionConcha = CharField('30.4. Descripción Concha', blank = True)
    esCarbon = models.BooleanField('30.5. Carbón No Superficial')
    descripcionCarbon = CharField('30.5. Descripción Carbón No Superficial', blank = True)
    esMito = models.BooleanField('30.6. Mitos')
    descripcionMito = CharField('30.6. Descripción Mitos', blank = True)
    esCementerio = models.BooleanField('30.7. Cementerios')
    descripcionCementerio = CharField('30.7. Descripción Cementerios', blank = True)
    esMonticulo = models.BooleanField('30.8. Montículos')
    descripcionMonticulo = CharField('30.8. Descripción Montículos', blank = True)
    otros = CharField('30.9. Otros', blank = True)
     
    abbr = 'mso'
 
    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = '30. Manifestaciones Asociadas'
         
    def __unicode__(self):
        return '' # '# ' + str(self.id)
		 
class ManifestacionesLitica(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesLitica')    
    esLitica = models.BooleanField('30.1. Lítica')
    descripcionLitica = CharField('Descripción', blank = True)
    
    abbr = 'mal'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = '30. Manifestaciones Asociadas'
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)		

class ManifestacionesCeramica(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesCeramica')    
    esCeramica = models.BooleanField('30.2. Cerámica')
    descripcionCeramica = CharField('Descripción', blank = True)    
    
    abbr = 'mac'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class ManifestacionesOseo(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesOseo')    
    esOseo = models.BooleanField('30.3. Oseo')
    descripcionOseo = CharField('Descripción', blank = True)

    abbr = 'mao'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)	
		
class ManifestacionesConcha(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesConcha')    
    esConcha = models.BooleanField('30.4. Concha')
    descripcionConcha = CharField('Descripción', blank = True)

    abbr = 'mco'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)	
		
class ManifestacionesCarbon(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesCarbon')    
    esCarbon = models.BooleanField('30.5. Carbón No Superficial')
    descripcionCarbon = CharField('Descripción', blank = True)

    abbr = 'mcar'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class ManifestacionesMito(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesMito')    
    esMito = models.BooleanField('30.6. Mitos')
    descripcionMito = CharField('Descripción', blank = True)

    abbr = 'mami'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)			

class ManifestacionesCementerio(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesCementerio')    
    esCementerio = models.BooleanField('30.7. Cementerios')
    descripcionCementerio = CharField('Descripción', blank = True)

    abbr = 'macm'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class ManifestacionesMonticulo(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesMonticulo')    
    esMonticulo = models.BooleanField('30.8. Montículos')
    descripcionMonticulo = CharField('Descripción', blank = True)

    abbr = 'mamn'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class ManifestacionesOtros(models.Model):

    yacimiento = models.OneToOneField(Yacimiento, related_name='ManifestacionesOtros')    
    otros = CharField('30.9. Otros', blank = True)

    abbr = 'maot'

    class Meta:
        verbose_name = '30. Manifestaciones Asociadas'
        verbose_name_plural = ''
        
    def __unicode__(self):
        return '' # '# ' + str(self.id)		
		
########################################################################################
# Diagrama de piedra
########################################################################################

class Piedra(models.Model):

    """Representa la información de la ficha pa, recoge la información básica"""

    yacimiento = models.ForeignKey(Yacimiento, related_name='Yacimiento')
    
    codigo = models.CharField('0 - Codigo de la roca', unique = True, max_length=20)#, primary_key=True)        
    nombre = CharField('1 - Nombre de la piedra', )
    manifiestacionAsociada = CharField('1.1 Manifestaciones asociadas', blank = True )
    nombreFiguras = CharField('2 - Nombre de las figuras',)    
    estado = models.ForeignKey(Estado, related_name='EstadoPied', blank = True, null = True)		
    numeroCaras = models.IntegerField('4 - Numero de Caras')
    numeroCarasTrajabadas = models.IntegerField('5 - Numero de caras trabajadas')
    
    def __unicode__(self):
        return short_text('Pa-' + self.codigo + '-' + self.nombre)
    
    abbr = 'pdr'

    class Meta:
        verbose_name = 'Roca'
        verbose_name_plural = 'Rocas'
		
class FotografiaPiedra (models.Model):
    
    piedra = models.ForeignKey(Piedra, related_name='FotografiaPiedra')
    archivo = models.ImageField('1.1. Fotografía - Archivo', upload_to='piedra/%Y_%m', null=True, blank=True)
    
    abbr = 'ftp'  

    class Meta:
        verbose_name = '1.1. Fotografia'
        verbose_name_plural = '1.1. Fotografias'
		
    def __unicode__(self):
        return '' # '# ' + str(self.id)		

class DimensionPiedra(models.Model):

    """Representa la información de las dimensiones de la piedra"""

    piedra = models.OneToOneField(Piedra, related_name='DimensionPiedra')
    
    altoMaximo =  models.DecimalField('7.a. Alto Maximo', max_digits=12, decimal_places=6)
    largoMaximo = models.DecimalField('7.b. Largo Maximo',max_digits=12, decimal_places=6)
    anchoMaximo = models.DecimalField('7.c. Ancho Maximo',max_digits=12, decimal_places=6)
    
    abbr = 'dip'
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)
		
    class Meta:
        verbose_name = 'Dimensiones de la piedra'
        verbose_name_plural = '7. Dimensiones de la piedra'

class CaraTrabajada(models.Model):

    """Representa la información de la ficha pa, referente a las caras trabajadas """
    
    ORIENTACION_CARA_TRABAJADA = (
        (0, '0 - Tope'),
        (1, '1 - Norte'),
        (2, '2 - Noreste'),
        (3, '3 - Este'),
        (4, '4 - Sureste'),
        (5, '5 - Sur'),
        (6, '6 - Suroeste'),
        (7, '7 - Oeste'),
        (8, '8 - Noroeste'),
        (9, '9 - Piso o plano inclinado'),
		(10, 'n - Desconocida')
    )
	
    piedra = models.ForeignKey(Piedra, related_name='CaraTrabajada')
    numero =  CharField('6a. Número de cara trabajada' )
    orientacion = models.IntegerField('6b. Orientación de la cara', choices = ORIENTACION_CARA_TRABAJADA)
    alto = models.DecimalField('7.1. Alto',max_digits=6, decimal_places=3)
    ancho = models.DecimalField('7.2. Ancho',max_digits=6, decimal_places=3)
    largo = models.DecimalField('7.3. Largo',max_digits=6, decimal_places=3)
    
    abbr = 'cat'

    def __unicode__(self):
        return '' # '# ' + str(self.id)
	
    class Meta:
        verbose_name = 'Cara trabajada'
        verbose_name_plural = '6-7. Caras trabajadas'

class UbicacionCaras(models.Model):

    """Representa la información de la ficha pa, referente a la ubicacion
    de las  caras trabajadas """

    LUMINOSIDAD = (
        (0, 'No tiene'),
        (1, 'Fótico'),
        (2, 'Escótico'),
    )

    piedra = models.OneToOneField(Piedra, related_name='UbicacionCaras')
    
    todaLaCaverna = models.BooleanField('8.1. Toda la caverna')
    areasEspecificas = models.BooleanField('8.2. Áreas específicas')
    salaPrincipal = models.BooleanField('8.2.1. Sala principal')
    otraSala = models.BooleanField('8.2.2. Otra sala')
    lagoInterior = models.BooleanField('8.2.3. Lago interior')
    claraboya = models.BooleanField('8.2.4. Claraboya')

    bocaPrincipal = models.DecimalField('8.3. Distancia Boca Principal',max_digits=12, decimal_places=6)
    luminosidad = models.IntegerField('8.3.1. Luminosidad', choices = LUMINOSIDAD)
    altura = models.DecimalField('8.3.2. Altura',max_digits=6, decimal_places=3)   
    requiereAndamiaje = models.BooleanField('8.3.2.1. ¿Requiere andamiaje?')
    
    abbr = 'uca'
	
    def __unicode__(self):
        return '' # '# ' + str(self.id)    
	
    class Meta:
        verbose_name = 'Ubic. cara trab. (cuevas/abrigos)'
        verbose_name_plural = '8. Ubic. caras trab. (cuevas/abrigos)'
        

class FigurasPorTipo(models.Model):

    """Representa la información de la ficha pa, referente a los conjuntos de
    figuras por tipo presentes en cada cara"""

    TIPO_FIGURA = (
        (1, '1 - Antropomorfas'),
        (2, '2 - Zoomorfas'),
        (3, '3 - Geométricas'),
        (4, '4 - Puntos Acoplados'),
        (5, '5 - Cupulas'),
        (6, '6 - Zoo-antropomorfas'),
        (7, '7 - Antropo-geométricas'),
        (8, '8 - Zoo-geométricas'),
        (9, '9 - Amoladores'),
        (10, '10 - Bateas'),
    )
	
    piedra = models.ForeignKey(Piedra, related_name='FigurasPorTipo')    
    numero =  CharField( '9.1. Número de cara trabajada (Punto 6)') 
    tipoFigura = models.IntegerField('9.2. Tipo de figura',choices = TIPO_FIGURA)	
    cantidad = CharField('9.3. Cantidad')  
    esCantidadInexacta = models.BooleanField('9.4. Cantidad Inexacta O Desconocida')	
    descripcion = CharField('9.5. Descripcion',)
    abbr = 'fpt'    
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)
		
    class Meta:
        verbose_name = 'Conjunto de figuras por Tipo'
        verbose_name_plural = '9. Conjuntos de figuras por tipo'

class EsquemaPorCara(models.Model):

    """Representa la información de la ficha pa, referente al esquema
    de la cara de la piedra"""

    piedra = models.ForeignKey(Piedra, related_name='EsquemaPorCara')    
    numero =  CharField( '10.1. Número de cara trabajada (Punto 6)')  
    textoCara = CharField('10.2. Cara del Volumen') 
    posicion = CharField('10.3. Posicion de las figuras') 
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)
		
    abbr = 'epc'

    class Meta:
        verbose_name = 'Esquema por cara'
        verbose_name_plural = '10. Esquemas por caras'

class ConexionFiguras(models.Model):

    """Representa la información de la ficha pa, referente a la conexion
    de las figuras en la piedra"""
    CONEXION_FIGURAS = (
        (1, '1 - Presencia de una sola figura'),
        (2, '2 - Menos del 10% interconectadas'),
        (3, '3 - 50% interconectadas'),
        (4, '4 - Mas del 80% interconectadas'),
    )    
    piedra = models.OneToOneField(Piedra, related_name='ConexionFiguras')    
    conexionFiguras = models.IntegerField('11. Conexion de figuras', choices = CONEXION_FIGURAS)
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)
		
    abbr = 'cnx'
    
    class Meta:
        verbose_name = 'Conexion de figuras'
        verbose_name_plural = '11. Conexion de figuras'

class Manifestaciones(models.Model):

    """Representa la información de la ficha pa, indicando el tipo de manifestacion"""

    piedra = models.OneToOneField(Piedra, related_name='Manifestaciones')
    
    tienePetroglifo = models.BooleanField('¿Tiene Petroglifos?')
    tienePinturaRupestre = models.BooleanField('¿Tiene Pintura Rupestre?')
    tieneAmoladores = models.BooleanField('¿Tiene Amoladores?')
    tienePuntosAcoplados = models.BooleanField('¿Tiene Puntos Acoplados?')
    tieneCupulas = models.BooleanField('¿Tiene Cupulas?')
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)
	
    abbr = 'man'
    
    class Meta:
        verbose_name = 'Manifestaciones de la piedra'
        verbose_name_plural = 'X. Manifestaciones de la piedra'
        

########################################################################################
# Tipos bases de multimedia
# Las clases que heredan de ella y son especificas a piedra o yacimiento
########################################################################################

# Tratamiento fotografico

class TratFoto(models.Model):

    """Representa el tratamiento dado a las fotografias recopiladas"""
    
    limpiezaCon = CharField('1. Limpieza con')
    rellenoSurcos = CharField('2. Relleno de surcos con')
    tratamientoDigital = CharField('3. Tratamiento digital')
    programaVersion = CharField('4. Programa/versión')
    otrosTratamientos = CharField('5. Otros tratamientos fotografía')

    def __unicode__(self):
        return '' # '# ' + str(self.id)
		
class TratFotoPiedra (TratFoto):

    """Representa el tratamiento dado a las fotografias recopiladas
    de las piedras"""

    piedra = models.OneToOneField(Piedra, related_name='TratFotoPiedra')
    
    abbr = 'tpp'
    
    class Meta:
        verbose_name = 'Tratamiento para fotografías'
        verbose_name_plural = '12. Tratamiento para fotografías'

# Fotografia

class Foto (models.Model):

    """Representa la información de la fotografia"""
    
    TIPO_FOTOGRAFIA = (
        (1, 'Aerea'),
        (2, 'No aerea'),
        (3, 'Satelital'),
    )

    negativo =  CharField('0a. Negativo', )
    tipoFotografia = models.IntegerField('0b. Tipo fotografia', choices = TIPO_FOTOGRAFIA)
    fecha = models.DateField('1. Fecha')
    fotografo  = CharField('2. Fotógrafo')
    institucion  = CharField('3. Institucion ')
    numReferencia = CharField('4. Nro de referencia')
    numRollo = CharField('5. Nro de rollo')
    numFoto = CharField('6. Nro de foto')
    numMarcaNegativo = CharField('7. Nro marca en negativo')
    esDeAnar = models.BooleanField('8. ¿Es de Anar?')
    numCopiaAnar = models.IntegerField('8.1. Num Copia ANAR')

    def __unicode__(self):
        return '' # '# ' + str(self.id)
	

class FotoPiedra (Foto):

    piedra = models.ForeignKey(Piedra, related_name='FotoPiedra')
    
    abbr = 'fop'
    
    class Meta:
        verbose_name =  '13.1 Mat. de apoyo fotográfico'
        verbose_name_plural = '13.1 Mat. de apoyo fotográfico'

# Representación gráfica de la piedra

class RepGrafPiedra (models.Model):

    """Representa la información de la ficha pa, agrupa los distintos tipos
    de reproducciones gráficas a escala natural y reducida"""

    piedra = models.ForeignKey(Piedra, related_name='RepGrafPiedra')
    
    numPiezas = models.IntegerField('a. Número de piezas')
    instituto  = CharField('b. Institución ', )
    persona  = CharField('c. Persona ', )
	
    def __unicode__(self):
        return '' # '# ' + str(self.id)
    
    abbr = 'rgp'

class EscNatPiedra(RepGrafPiedra):

    TIPO_REPRODUCCION_NATURAL = (
        (1, '1 - Plana'),
        (2, '2 - Frotage'),
        (3, '3 - Calco'),
        (4, '4 - Tridimensional'),
        (5, '5 - Resina'),
        (6, '6 - Yeso'),
        (7, '7 - Papel de arroz'),
    )
    tipoReproduccion = models.IntegerField('13.2.1. Reproducción gráfica', choices = TIPO_REPRODUCCION_NATURAL)

    abbr = 'enp'

    class Meta:
        verbose_name = 'Reproducción gráf. escala natural'
        verbose_name_plural = '13.2. Reproducción gráf. escala natural'
    
class EscRedPiedra(RepGrafPiedra):

    """Representa la información de la ficha pa, de reproducciones gráficas
    a escala reducida"""
        
    TIPO_REPRODUCCION_REDUCIDA = (
        (1, '1 - Dibujo'),
        (2, '2 - Matriz'),
    )
    tipoReproduccion = models.IntegerField('13.3.1. Reproducción gráfica', choices = TIPO_REPRODUCCION_REDUCIDA)
    
    abbr = 'erp'

    class Meta:
        verbose_name = 'Reproducción gráf. escala reducida'
        verbose_name_plural = '13.3. Reproducción gráf. escala reducida'

# Bibliografia

class Bibliografia(models.Model):

    TIPO_MAPA = (
        (1, '1 - Radar'),
        (2, '2 - Satelital'),
    )

    """Representa la bibliografia de un yacimiento o una piedra """
	
    def __unicode__(self):
        return '' # '# ' + str(self.id)

class BibYacimiento(Bibliografia):

    yacimiento = models.ForeignKey(Yacimiento, related_name='BibYacimiento')
    codigo = CharField('31.1.1. Código', blank = True)
    titulo = CharField('31.1.2. Título', blank = True)
    autor  = CharField('31.1.3. Autor ', blank = True)
    ano = CharField('31.1.4. Fecha', blank = True)
    institucion  = CharField('31.1.5. Institución', blank = True)
    conDibujo = models.BooleanField('31.1.6. Con dibujo',)
    archivo = models.ImageField('31.1.6.1. Dibujo - Archivo', upload_to='bibliografia_yac/%Y_%m', null=True, blank=True)
    
    esFotografia = models.BooleanField('31.1.7. Con fotografía')
    escolor = models.BooleanField('31.1.7.1. Color')
    esBlancoYNegro = models.BooleanField('31.1.7.2. B/N')
    esDiapositiva = models.BooleanField('31.1.7.3. Diapositiva')
    esPapel = models.BooleanField('31.1.7.4. Papel')
    esDigital = models.BooleanField('31.1.7.5. Digital')
    esNegativo = models.BooleanField('31.1.7.6. Negativo')
    descripcion  = CharField('31.1.7.7. Con mapa ', blank = True)
    tipoMapa = models.IntegerField('31.1.7.8. Tipo de mapa', choices = Bibliografia.TIPO_MAPA, blank = True,null = True)
	
    abbr = 'biy'
    
    class Meta:
        verbose_name = 'Bibliografía'
        verbose_name_plural = '31.1. Bibliografía'

class BibPiedra(Bibliografia):

    piedra = models.ForeignKey(Piedra, related_name='BibPiedra')
    codigo = CharField('13.4.1. Código', blank = True)
    titulo = CharField('13.4.2. Título', blank = True)
    autor  = CharField('13.4.3. Autor ', blank = True)
    ano = CharField('13.4.4. Fecha', blank = True)	
    institucion  = CharField('13.4.5. Institución', blank = True)
    conDibujo = models.BooleanField('13.4.6. Con dibujo')
    archivo = models.ImageField('13.4.6.1. Dibujo - Archivo', upload_to='bibliografia_pie/%Y_%m', null=True, blank=True)
    
    esFotografia = models.BooleanField('13.4.7. Con fotografía')
    escolor = models.BooleanField('13.4.7.1. Color')
    esBlancoYNegro = models.BooleanField('13.4.7.2. B/N')
    esDiapositiva = models.BooleanField('13.4..7.3. Diapositiva')
    esPapel = models.BooleanField('13.4.7.4. Papel')
    esDigital = models.BooleanField('13.4.7.5. Digital')
    esNegativo = models.BooleanField('13.4.7.6. Negativo')
    descripcion  = CharField('13.4.7.7. Con mapa ', blank = True)
    tipoMapa = models.IntegerField('13.4.7.8. Tipo de mapa', choices = Bibliografia.TIPO_MAPA,blank = True,null = True)
	
    abbr = 'bip'
    
    class Meta:
        verbose_name = 'Bibliografía'
        verbose_name_plural = '13.4. Bibliografía'




# Material audiovisual     

class MatAudioVisual (models.Model):

    formato = CharField('1. Formato', )
    archivo = models.FileField('2. Material AV - Archivo', upload_to='audiovisual/%Y_%m', null=True, blank=True)
	
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class MatAVYacimiento(MatAudioVisual):

    yacimiento = models.ForeignKey(Yacimiento, related_name='MatAVYacimiento')
    
    abbr = 'avy'
    
    class Meta:
        verbose_name = 'Material audiovisual'
        verbose_name_plural = '31.2. Material audiovisual'

class MatAVPiedra(MatAudioVisual):

    piedra = models.ForeignKey(Piedra, related_name='MatAVPiedra')
    
    abbr = 'avp'

    class Meta:
        verbose_name = 'Material audiovisual'
        verbose_name_plural = '13.5. Material audiovisual'
    
# Videos 

class Video (models.Model):

    anio = models.IntegerField('0. Año')
    formato = CharField('1. Formato',)
    titulo = CharField('2. Titulo')
    autor = CharField('3. Autor')    
    institucion = CharField('4. Institucion',)
    numReferencia = models.IntegerField('5. Nro de referencia')
    isFromAnar = models.BooleanField('6. ¿Es de ANAR?')
    numCopia = models.IntegerField('6.1. Nro de copia')
    archivo = models.FileField('7. Video - Archivo', upload_to='video/%Y_%m', null=True, blank=True)
	
    def __unicode__(self):
        return '' # '# ' + str(self.id)	
    
class VideoYacimiento (Video) :

    yacimiento = models.ForeignKey(Yacimiento, related_name='VideoYacimiento')
    
    abbr = 'vdy'
    
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = '31.3. Videos'

class VideoPiedra (Video) :

    piedra = models.ForeignKey(Piedra, related_name='VideoPiedra')
    
    abbr = 'vdp'
    
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = '13.6. Videos'

# Película

class Pelicula (Video):
    
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class PeliYacimiento (Pelicula):
    
    yacimiento = models.ForeignKey(Yacimiento, related_name='PeliYacimiento')
    
    abbr = 'ply'
    
    class Meta:
        verbose_name = 'Película'
        verbose_name_plural = '31.4. Películas'

class PeliculaPiedra (Pelicula):

    piedra = models.ForeignKey(Piedra, related_name='PeliculaPiedra')
    
    abbr = 'plp'
    
    class Meta:
        verbose_name = 'Película'
        verbose_name_plural = '13.7. Películas'

# Página Web

class PaginaWeb (models.Model):
    
    direccionURL = models.URLField ('0. URL de página web')
	
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class PaginaWebYac (PaginaWeb):

    yacimiento = models.ForeignKey(Yacimiento, related_name='PaginaWebYac')
    
    abbr = 'pwy'
    
    class Meta:
        verbose_name = 'Página Web'
        verbose_name_plural = '31.5. Página Web'

class PaginaWebPiedra (PaginaWeb):

    piedra = models.ForeignKey(Piedra, related_name='PaginaWebPiedra')
    
    abbr = 'pwp'
    
    class Meta:
        verbose_name = 'Página Web'
        verbose_name_plural = '13.8. Página Web'

# Multimedia

class Multimedia (models.Model):

    tecnica = CharField('1. Técnica', )
    archivo = models.FileField('2. Multimedia - Archivo', upload_to='multimedia/%Y_%m', null=True, blank=True)
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class MultimediaYac (Multimedia):

    yacimiento = models.ForeignKey(Yacimiento, related_name='MultimediaYac')
    
    abbr = 'mmy'
    
    class Meta:
        verbose_name = 'Multimedia'
        verbose_name_plural = '31.6. Multimedia'

class MultimediaPiedra (Multimedia):

    piedra = models.ForeignKey(Piedra, related_name='MultimediaPiedra')
    
    abbr = 'mmp'
    
    class Meta:
        verbose_name = 'Multimedia'
        verbose_name_plural = '13.9. Multimedia'

# Obtencion de informacion

class ObtencionInfo (models.Model):

    prospeccion = models.BooleanField('1. Prospección sistemática')
    comunicacion = models.BooleanField('2. Comunicación personal')
    nombre = CharField('2.1. Nombre')
    direccion = CharField('2.2. Dirección', blank = True)
    telefono = CharField('2.3. Telefono/Fax',  blank = True)
    telefonoCel = CharField('2.4. Telefono celular',  blank = True)
    mail = models.EmailField('2.5. Correo electrónico', blank = True)
    paginaWeb = models.URLField('2.6. Página Web', blank = True)
    twitter = CharField('2.7. Twitter',  blank = True)
    nombreFacebook = CharField('2.8. Perfil Facebook',  blank = True)
    blog = models.URLField('2.9. Blog', blank = True)
    fecha = models.DateField('2.10. Fecha')
    verificado = models.BooleanField('2.3. Verificado en el campo')

    def __unicode__(self):
        return '' # '# ' + str(self.id)	
	
class ObtInfoYac (ObtencionInfo):

    yacimiento = models.ForeignKey(Yacimiento, related_name='ObtInfoYac')
    
    abbr = 'oiy'
    
    class Meta:
        verbose_name = 'Información obtenida por'
        verbose_name_plural = '32. Información obtenida por'

class ObtInfoPiedra (ObtencionInfo):

    piedra = models.ForeignKey(Piedra, related_name='ObtInfoPiedra')
    
    abbr = 'oip'

    class Meta:
        verbose_name = 'Información obtenida por'
        verbose_name_plural = '14. Información obtenida por'
    
        
# Otros valores

class OtrosValores(models.Model):

    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class OtrosValYac(OtrosValores):

    yacimiento = models.ForeignKey(Yacimiento, related_name='OtrosValYac')
    texto = CharField('33. Otros valores del sitio', blank = True)
    abbr = 'ovy'
    
    class Meta:
        verbose_name = 'Otros valores del sitio'
        verbose_name_plural = ''

class OtrosValPiedra(OtrosValores):

    piedra = models.ForeignKey(Piedra, related_name='OtrosValPiedra')
    texto = CharField('0. Otros valores', blank = True)
    abbr = 'ovp'
    
    class Meta:
        verbose_name = 'Otros valores de la piedra'
        verbose_name_plural = '15. Otros valores de la piedra'

# Observaciones

class Observaciones(models.Model):

    texto = CharField('0. Observaciones',)
	
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class ObservacionesYac(Observaciones):

    yacimiento = models.ForeignKey(Yacimiento, related_name='ObservacionesYac')
    
    abbr = 'oya'
    
    class Meta:
        verbose_name = 'Observaciones'
        verbose_name_plural = '34. Observaciones'

class ObservacPiedra(Observaciones):

    piedra = models.ForeignKey(Piedra, related_name='ObservacPiedra')
    
    abbr = 'opi'
    
    class Meta:
        verbose_name = 'Observaciones'
        verbose_name_plural = '16. Observaciones'

# Llenado de la ficha

class LlenadoPor(models.Model):

    nombre = CharField('1. Llenada por: ', blank = True)
    fecha = models.DateField('2. Fecha',blank = True, null= True)
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class LlenadoYac(LlenadoPor):    

    yacimiento = models.ForeignKey(Yacimiento, related_name='LlenadoYac')
    
    abbr = 'ypy'

    class Meta:
        verbose_name = 'Ficha llenada por'
        verbose_name_plural = '35. Ficha llenada Por'
    
class LlenadoPiedra(LlenadoPor):    

    piedra = models.ForeignKey(Piedra, related_name='LlenadoPiedra')
    
    abbr = 'ypp'
    
    class Meta:
        verbose_name = 'Ficha llenada por'
        verbose_name_plural = '17. Ficha llenada por'

# Supervision de la ficha

class SupervisadoPor(models.Model):

    nombre = CharField('1. Supervisada por: ', blank = True)
    fecha = models.DateField('2. Fecha', blank = True, null= True)
	
    def __unicode__(self):
        return '' # '# ' + str(self.id)	

class SupervisadoYac(SupervisadoPor):
    
    yacimiento = models.ForeignKey(Yacimiento, related_name='SupervisadoYac')
    
    abbr = 'spy'
    
    class Meta:
        verbose_name = 'Ficha Supervisada Por'
        verbose_name_plural = '36. Ficha Supervisada Por'

class SupervisadoPiedra(SupervisadoPor):
    
    piedra = models.ForeignKey(Piedra, related_name='SupervisadoPiedra')
    
    abbr = 'spp'    

    class Meta:
        verbose_name = 'Ficha Supervisada Por'
        verbose_name_plural = '18. Ficha Supervisada Por'

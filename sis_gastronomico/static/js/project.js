/* Project specific Javascript goes here. */
$('.datepicker').each((index, element) => {
  $(element).click(function (e){e.preventDefault();});
  $(element).attr('placeholder', 'Ingrese una Fecha');
  let fecha_input = $(element).val().split('-');
  let fecha = '';
  if (fecha_input[0] != '')
    fecha = new Date(fecha_input[0], fecha_input[1]-1, fecha_input[2]);
  $(element).datepicker({
      format: 'yyyy-mm-dd',
      setDefaultDate: true,
      defaultDate: fecha,
      autoClose: true,
      yearRange: [1940, new Date().getFullYear()],
      maxDate: new Date(),
      i18n: {
      months: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
      monthsShorts: ['Ene','Feb','Mar','','Abr','','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
      weekdays: ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado'],
      weekdaysShort: ['Dom','Lun','Mar','Mie','Jue','Vie','Sab'],
      weekdaysAbbrev: ['D','L','M','X','J','V','S']
      }
  });
});
$('select').formSelect();
$('.timepicker').timepicker({
  autoClose: true,
  twelveHour: false
});
$('.sidenav').sidenav();
$('.collapsible').collapsible();

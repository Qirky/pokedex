var resetFilterForm = function(){
  var form = $("#filter-form");
  form.find('input, select').not('input:checkbox').val('');
  form.find('select option:selected').removeAttr('selected');
  form.find('input:checkbox').prop("checked", false);
}

var toggleSelectAll = function() {
  if ($(this).prop("checked")) {
    $('.pokemon-checkbox').prop('checked', true);
  } else {
    $('.pokemon-checkbox').prop('checked', false);
  }
  $('.pokemon-checkbox').trigger('change');
}

var checkExportButtonStatus = function() {
  if ($('.pokemon-checkbox:checkbox:checked').length > 0){
    $('.btn-download').prop('disabled', false);
  } else {
    $('.btn-download').prop('disabled', true);
  }
}

var checkMutuallyExclusiveInputStatus = function() {
  $('.mutually-exclusive').not(this).prop('checked', false);
}

var selectPokemonRow = function() {
  var checkbox = $(this).find('input:checkbox');
  checkbox.prop('checked', !checkbox.prop('checked'));
  checkbox.trigger('change');
}

$(document).ready(function() {
  $('#btn-reset-filter-form').click(resetFilterForm);
  $('#checkbox-select-all').click(toggleSelectAll);
  $('.pokemon-checkbox').on('change', checkExportButtonStatus);
  $('.mutually-exclusive').on('change', checkMutuallyExclusiveInputStatus);
  $('#tbl-pokemon tr.pokemon-row').click(selectPokemonRow);
  $('#tbl-pokemon tr.pokemon-row input:checkbox').click(function(e){
    e.stopPropagation();
  })
  checkExportButtonStatus();
});

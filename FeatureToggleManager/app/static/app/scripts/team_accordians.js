
function generate_team_accordian(team_id) {
    var team_accordian = '<div class="panel-heading" role="tab" id="heading' + team_id + '">' +
        '<h4 class="panel-title">' +
        '<a role="button" data-toggle="collapse" href="#collapse' + team_id + '" aria-expanded="true" aria-controls="collapse' + team_id + '">' + team_id + '</a>' +
        '</h4>' +
        '</div>' +
        '<div id="collapse' + team_id + '" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="heading' + team_id + '">' +
        '<div class="panel-body">' +
        '<div class="table-responsive">' +
        '<table id = "' + team_id + '_table" class="display table table-striped table-bordered" ></table >' +
        '</div >';
    $("#team_accordians").append(team_accordian);
}
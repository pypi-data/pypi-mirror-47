import smashggpy.queries.Event_Queries as queries
from smashggpy.util.Logger import Logger
from smashggpy.common.Common import flatten
from smashggpy.util.NetworkInterface import NetworkInterface as NI
from smashggpy.util.ThreadFactory import ThreadFactory


class Event(object):

    def __init__(self, id, name, slug, state, start_at, num_entrants,
                 check_in_buffer, check_in_duration, check_in_enabled,
                 is_online, team_name_allowed, team_management_deadline):
        self.id = id
        self.name = name
        self.slug = slug
        self.state = state
        self.start_at = start_at
        self.num_entrants = num_entrants
        self.check_in_buffer = check_in_buffer
        self.check_in_duration = check_in_duration
        self.check_in_enabled = check_in_enabled
        self.is_online = is_online
        self.team_name_allowed = team_name_allowed
        self.team_management_deadline = team_management_deadline

    @staticmethod
    def get(tournament_slug: str, event_slug: str):
        assert (tournament_slug is not None), "Event.get cannot have None for tournament_slug parameter"
        assert (event_slug is not None), "Event.get cannot have None for event_slug parameter"
        slug = "tournament/{0}/event/{1}".format(tournament_slug, event_slug)
        data = NI.query(queries.get_event_by_slugs, {"slug": slug})

        try:
            base_data = data['data']['event']
            return Event.parse(base_data)
        except AttributeError as e:
            raise Exception("No event data came back for tournament {} and event {}".format(tournament_slug, event_slug))

    @staticmethod
    def get_by_id(id: int):
        assert (id is not None), "Event.get_by_id cannot have None for id parameter"
        data = NI.query(queries.get_event_by_id, {'id': id})

        try:
            base_data = data['data']['event']
            return Event.parse(base_data)
        except AttributeError as e:
            raise Exception("No event data came back for event with id {}".format(id))

    @staticmethod
    def parse(data):
        assert (data is not None), "Event.parse cannot have None for data parameter"
        return Event(
            data['id'],
            data['name'],
            data['slug'],
            data['state'],
            data['startAt'],
            data['numEntrants'],
            data['checkInBuffer'],
            data['checkInDuration'],
            data['checkInEnabled'],
            data['isOnline'],
            data['teamNameAllowed'],
            data['teamManagementDeadline']
        )

    def get_phases(self):
        assert (self.id is not None), "event id cannot be None if calling get_phases"
        Logger.info('Getting Phases for Event: {0}:{1}'.format(self.id, self.name))
        data = NI.query(queries.get_event_phases, {'id': self.id})

        try:
            phases_data = data['data']['event']['phases']
            return [Phase.parse(phase_data) for phase_data in phases_data]
        except AttributeError as e:
            raise Exception("No phase data pulled back for event {} {}".format(self.id, self.name))

    def get_phase_groups(self):
        assert (self.id is not None), "event id cannot be None if calling get_phase_groups"
        Logger.info('Getting Phase Groups for Event: {0}:{1}'.format(self.id, self.name))
        data = NI.query(queries.get_event_phase_groups, {'id': self.id})

        try:
            phase_groups_data = data['data']['event']['phaseGroups']
            return [PhaseGroup.parse(phase_group_data) for phase_group_data in phase_groups_data]
        except AttributeError as e:
            raise Exception("No phase group data pulled back for event {} {}".format(self.id, self.name))

    def get_attendees(self):
        Logger.info('Getting Attendees for Event: {0}:{1}'.format(self.id, self.name))
        phase_groups = self.get_phase_groups()
        attendees = flatten([phase_group.get_attendees() for phase_group in phase_groups])
        return attendees

    def get_entrants(self):
        Logger.info('Getting Entrants for Event: {0}:{1}'.format(self.id, self.name))
        phase_groups = self.get_phase_groups()
        entrants = flatten([phase_group.get_entrants() for phase_group in phase_groups])
        return entrants

    def get_sets(self):
        Logger.info('Getting Sets for Event: {0}:{1}'.format(self.id, self.name))
        phase_groups = self.get_phase_groups()
        sets = flatten([phase_group.get_sets() for phase_group in phase_groups])
        return sets

    def get_incomplete_sets(self):
        Logger.info('Getting Incomplete Sets for Event: {0}:{1}'.format(self.id, self.name))
        sets = self.get_sets()
        incomplete_sets = []
        for ggset in sets:
            if ggset.get_is_completed() is False:
                incomplete_sets.append(ggset)
        return incomplete_sets

    def get_completed_sets(self):
        Logger.info('Getting Completed Sets for Event: {0}:{1}'.format(self.id, self.name))
        sets = self.get_sets()
        complete_sets = []
        for ggset in sets:
            if ggset.get_is_completed() is True:
                complete_sets.append(ggset)
        return complete_sets

    # GETTERS
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_slug(self):
        return self.slug

    def get_state(self):
        return self.state

    def get_start_at(self):
        return self.start_at

    def get_num_entrants(self):
        return self.num_entrants

    def get_check_in_buffer(self):
        return self.check_in_buffer

    def get_check_in_duration(self):
        return self.check_in_duration

    def get_check_in_enabled(self):
        return self.check_in_enabled

    def get_is_online(self):
        return self.is_online

    def get_team_name_allowed(self):
        return self.team_name_allowed

    def get_team_management_deadline(self):
        return self.team_management_deadline


from smashggpy.models.Phase import Phase
from smashggpy.models.PhaseGroup import PhaseGroup
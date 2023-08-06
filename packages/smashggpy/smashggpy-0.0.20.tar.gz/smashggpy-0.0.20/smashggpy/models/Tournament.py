import smashggpy.queries.Tournament_Queries as queries
from smashggpy.util.Logger import Logger
from smashggpy.common.Common import flatten
from smashggpy.util.NetworkInterface import NetworkInterface as NI
from smashggpy.models.Venue import Venue
from smashggpy.models.Organizer import Organizer

class Tournament(object):

    def __init__(self, id, name, slug, start_time, end_time, timezone, venue, organizer):
        self.id = id
        self.name = name
        self.slug = slug
        self.start_time = start_time
        self.end_time = end_time
        self.timezone = timezone
        self.venue = venue
        self.organizer = organizer

    @staticmethod
    def get(slug: str):
        assert (slug is not None), "Tournament.get must have a slug parameter"
        data = NI.query(queries.get_tournament_by_slug, {'slug': slug})

        if 'errors' in data:
            raise Exception('Error occurred in pulling tournament {}, {}'.format(slug, data['errors']))

        try:
            base_data = data['data']['tournament']
            return Tournament.parse(base_data)
        except AttributeError as e:
            raise Exception('No data returned for tournament {}'.format(slug))


    @staticmethod
    def get_by_id(id: int):
        assert (id is not None), "Tournament.get_by_id must have an id parameter"
        data = NI.query(queries.get_tournament_by_id, {'id': id})

        try:
            base_data = data['data']['tournament']
            return Tournament.parse(base_data)
        except AttributeError as e:
            raise Exception('No data returned for tournament id {}'.format(id))

    @staticmethod
    def parse(data):
        assert (data is not None), "Tournament.parse must have a data parameter"
        return Tournament(
            data['id'],
            data['name'],
            data['slug'],
            data['startAt'],
            data['endAt'],
            data['timezone'],
            Venue.parse(data),
            Organizer.parse(data)
        )

    def get_events(self):
        assert (self.id is not None), "tournament id cannot be None if calling get_events"
        data = NI.query(queries.get_tournament_events, {'id': self.id})

        try:
            base_data = data['data']['tournament']['events']
            return [Event.parse(event_data) for event_data in base_data]
        except AttributeError as e:
            raise Exception('No event data retrieved for tournament {}'.format(self.slug))

    def get_phases(self):
        assert (self.id is not None), "tournament id cannot be None if calling get_phases"
        data = NI.query(queries.get_tournament_phases, {'id': self.id})

        try:
            base_events = data['data']['tournament']['events']
            phases = []
            for event in base_events:
                try:
                    for event_phase in event['phases']:
                        phases.append(Phase.parse(event_phase))
                except AttributeError as inner_e:
                    raise Exception("No phase data pulled back for tournament {}".format(self.slug))
            return phases
        except AttributeError as e:
            raise Exception("No event data pulled back for tournament {}".format(self.slug))

    def get_phase_groups(self):
        assert (self.id is not None), "tournament id cannot be None if calling get_phase_groups"
        data = NI.query(queries.get_tournament_phase_groups, {'id': self.id})

        try:
            base_events = data['data']['tournament']['events']
            phase_groups = []
            for event in base_events:
                try:
                    for event_phase_groups in event['phaseGroups']:
                        phase_groups.append(PhaseGroup.parse(event_phase_groups))
                except AttributeError as inner_e:
                    raise Exception("No phase group data pulled back for tournament {}".format(self.slug))
            return phase_groups
        except AttributeError as e:
            raise Exception("No event data pulled back for tournament {}".format(self.slug))

    def get_attendees(self):
        Logger.info('Getting Attendees for Tournament: {0}:{1}'.format(self.id, self.name))
        phase_groups = self.get_phase_groups()
        attendees = flatten([phase_group.get_attendees() for phase_group in phase_groups])
        return attendees

    def get_entrants(self):
        Logger.info('Getting Entrants for Tournament: {0}:{1}'.format(self.id, self.name))
        Logger.warning('Aggregate queries ')
        phase_groups = self.get_phase_groups()
        entrants = flatten([phase_group.get_entrants() for phase_group in phase_groups])
        return entrants

    def get_sets(self):
        Logger.info('Getting Sets for Tournament: {0}:{1}'.format(self.id, self.name))
        phase_groups = self.get_phase_groups()
        sets = flatten([phase_group.get_sets() for phase_group in phase_groups])
        return sets

    def get_incomplete_sets(self):
        Logger.info('Getting Incomplete Sets for Tournament: {0}:{1}'.format(self.id, self.name))
        sets = self.get_sets()
        incomplete_sets = []
        for ggset in sets:
            if ggset.get_is_completed() is False:
                incomplete_sets.append(ggset)
        return incomplete_sets

    def get_completed_sets(self):
        Logger.info('Getting Completed Sets for Tournament: {0}:{1}'.format(self.id, self.name))
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

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_timezone(self):
        return self.timezone

    def get_venue(self):
        return self.venue

    def get_organizer(self):
        return self.organizer


from smashggpy.models.Event import Event
from smashggpy.models.Phase import Phase
from smashggpy.models.PhaseGroup import PhaseGroup

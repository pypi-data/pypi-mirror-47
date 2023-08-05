"""Provides class that allows access to an SQL format CampaignDB.
"""
import json
import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .base import BaseCampaignDB
from easyvvuq.sampling.base import BaseSamplingElement
from easyvvuq.encoders.base import BaseEncoder
from easyvvuq.decoders.base import BaseDecoder
from easyvvuq.collate.base import BaseCollationElement

__copyright__ = """

    Copyright 2018 Robin A. Richardson, David W. Wright

    This file is part of EasyVVUQ

    EasyVVUQ is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EasyVVUQ is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
__license__ = "LGPL"

logger = logging.getLogger(__name__)

Base = declarative_base()


class CampaignTable(Base):
    """An SQLAlchemy schema for the campaign information table.
    """
    __tablename__ = 'campaign_info'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    easyvvuq_version = Column(String)
    campaign_dir_prefix = Column(String)
    campaign_dir = Column(String)
    runs_dir = Column(String)


class AppTable(Base):
    """An SQLAlchemy schema for the app table.
    """
    __tablename__ = 'app'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    input_encoder = Column(String)
    output_decoder = Column(String)
    params = Column(String)
    fixtures = Column(String)
    collation = Column(String)


class RunTable(Base):
    """An SQLAlchemy schema for the run table.
    """
    __tablename__ = 'run'
    id = Column(Integer, primary_key=True)
    run_name = Column(String)
    app = Column(Integer, ForeignKey('app.id'))
    # Parameter values for this run
    params = Column(String)
    # TODO: Consider making status an ENUM to enforce relevant EasyVVUQ values
    status = Column(String)
    run_dir = Column(String)
    campaign = Column(Integer, ForeignKey('campaign_info.id'))
    sample = Column(Integer, ForeignKey('sample.id'))


class SamplerTable(Base):
    """An SQLAlchemy schema for the run table.
    """
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    sampler = Column(String)


class CampaignDB(BaseCampaignDB):

    def __init__(self, location=None, new_campaign=False, name=None,
                 info=None):

        if location is not None:
            self.engine = create_engine(location)
        else:
            self.engine = create_engine('sqlite://')

        session_maker = sessionmaker(bind=self.engine)

        self.session = session_maker()

        if new_campaign:
            if info is None:
                raise RuntimeError('No information provided to create'
                                   'database')
            if info.name != name:
                message = (f'Information for campaign {info.name} given '
                           f'for campaign database {name}')
                logging.critical(message)
                raise RuntimeError(message)
            Base.metadata.create_all(self.engine)

            self.session.add(CampaignTable(**info.to_dict(flatten=True)))
            self.session.commit()
            self._next_run = 1
        else:
            info = self.session.query(
                CampaignTable).filter_by(name=name).first()
            if info is None:
                raise ValueError('Campaign with the given name not found.')

            self._next_run = self.session.query(RunTable).count() + 1

    def app(self, name=None):
        """
        Get app information. Specific applications selected by `name`,
        otherwise first entry in database 'app' selected.

        Parameters
        ----------
        name : str or None
            Name of selected app, if `None` given then first app will be
            selected.

        Returns
        -------
        dict:
            Application information.
        """

        # TODO: Find efficient way for this
        if name is None:
            logging.warning('No app name provided so using first app '
                            'in database')
            selected = self.session.query(AppTable).all()
        else:
            selected = self.session.query(AppTable).filter_by(name=name).all()

        if len(selected) == 0:
            message = f'No entry for app: ({name}).'
            logger.critical(message)
            raise RuntimeError(message)
        if len(selected) > 1:
            message = f'Too many apps called: ({name}).'
            logger.critical(message)
            raise RuntimeError(message)

        selected_app = selected[0]

        app_dict = {
            'id': selected_app.id,
            'name': selected_app.name,
            'input_encoder': selected_app.input_encoder,
            'output_decoder': selected_app.output_decoder,
            'params': json.loads(selected_app.params),
            'fixtures': json.loads(selected_app.fixtures),
            'collation': json.loads(selected_app.collation)
        }

        return app_dict

    def add_app(self, app_info):
        """
        Add application to the 'app' table.

        Parameters
        ----------
        app_info: AppInfo
            Application definition.

        Returns
        -------

        """

        # Check that no app with same name exists
        name = app_info.name
        selected = self.session.query(
            AppTable).filter_by(name=name).all()
        if len(selected) > 0:
            message = (
                f'There is already an app in this database with name {name}'
                f'(found {len(selected)}).'
            )
            logger.critical(message)
            raise RuntimeError(message)

        app_dict = app_info.to_dict(flatten=True)

        db_entry = AppTable(**app_dict)

        self.session.add(db_entry)
        self.session.commit()

    def add_sampler(self, sampler_element):
        """
        Add new Sampler to the 'sampler' table.

        Parameters
        ----------
        sampler_element: BaseSamplingElement

        Returns
        -------

        """
        db_entry = SamplerTable(sampler=sampler_element.serialize())

        self.session.add(db_entry)
        self.session.commit()

        return db_entry.id

    def resurrect_sampler(self, sampler_id):
        serialized_sampler = self.session.query(SamplerTable).get(sampler_id).sampler
        sampler = BaseSamplingElement.deserialize(serialized_sampler)
        return sampler

    def resurrect_app(self, app_name):
        app_info = self.app(app_name)
        encoder = BaseEncoder.deserialize(app_info['input_encoder'])
        decoder = BaseDecoder.deserialize(app_info['output_decoder'])
        collater = BaseCollationElement.deserialize(app_info['collation'])
        return encoder, decoder, collater

    def update_sampler(self, sampler_id, sampler_element):
        selected = self.session.query(SamplerTable).get(sampler_id)
        selected.sampler = sampler_element.serialize()
        self.session.commit()

    def add_run(self, run_info=None, prefix='Run_'):
        """
        Add run to the `runs` table in the database.

        Parameters
        ----------
        run_info: RunInfo
            Contains relevant run fields: params, status (where in the
            EasyVVUQ workflow is this RunTable), campaign (id number),
            sample, app
        prefix: str
            Prefix for run id

        Returns
        -------

        """

        run_info.run_name = f"{prefix}{self._next_run}"

        run = RunTable(**run_info.to_dict(flatten=True))
        self.session.add(run)
        self.session.commit()
        self._next_run += 1

    @staticmethod
    def _run_to_dict(run_row):
        """
        Convert the provided row from 'runs' table into a dictionary

        Parameters
        ----------
        run_row: RunTable
            Information on a particular run in the database.

        Returns
        -------
        dict:
            Contains run information (keys = run_name, params, status, sample,
            campaign and app)

        """

        run_info = {
            'run_name': run_row.run_name,
            'params': json.loads(run_row.params),
            'status': run_row.status,
            'sample': run_row.sample,
            'campaign': run_row.campaign,
            'app': run_row.app,
            'run_dir': run_row.run_dir
        }

        return run_info

    def run(self, run_name, campaign=None, sampler=None):
        """
        Get the information for a specified run.

        Parameters
        ----------
        run_name: str
            Name of run to filter for.
        campaign:  int or None
            Campaign id to filter for.
        sampler: int or None
            Sampler id to filter for.

        Returns
        -------
        dict
            Containing run information (run_name, params, status, sample,
            campaign, app)
        """

        if campaign is None and sampler is None:
            selected = self.session.query(
                RunTable).filter_by(run_name=run_name)
        elif campaign is not None and sampler is not None:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, campaign=campaign, sample=sampler)
        elif campaign is not None:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, campaign=campaign)
        else:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, sample=sampler)

        if selected.count() != 1:
            logging.warning('Multiple runs selected - using the first')

        selected = selected.first()

        return self._run_to_dict(selected)

    def set_dir_for_run(self, run_name, run_dir, campaign=None, sampler=None):
        if campaign is None and sampler is None:
            selected = self.session.query(
                RunTable).filter_by(run_name=run_name)
        elif campaign is not None and sampler is not None:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, campaign=campaign, sample=sampler)
        elif campaign is not None:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, campaign=campaign)
        else:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, sample=sampler)

        if selected.count() != 1:
            logging.warning('Multiple runs selected - using the first')

        selected = selected.first()

        selected.run_dir = run_dir
        self.session.commit()

    def set_run_status(self, run_name, status, campaign=None, sampler=None):
        if campaign is None and sampler is None:
            selected = self.session.query(
                RunTable).filter_by(run_name=run_name)
        elif campaign is not None and sampler is not None:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, campaign=campaign, sample=sampler)
        elif campaign is not None:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, campaign=campaign)
        else:
            selected = self.session.query(RunTable).filter_by(
                run_name=run_name, sample=sampler)

        if selected.count() != 1:
            logging.warning('Multiple runs selected - using the first')

        selected = selected.first()

        selected.status = status
        self.session.commit()

    def campaigns(self):
        """Get list of campaigns for which information is stored in the
        database.

        Returns
        -------
        list:
            Campaign names.
        """

        return [c.name for c in self.session.query(CampaignTable).all()]

    def _get_campaign_info(self, campaign_name=None):
        """
        Parameters
        ----------
        campaign_name: str
            Name of campaign to select

        Returns
        -------

        """

        query = self.session.query(CampaignTable)

        if campaign_name is None:
            campaign_info = query
        else:
            campaign_info = query.filter_by(name=campaign_name).all()

        if campaign_info.count() > 1:
            logger.warning(
                'More than one campaign selected - using first one.')
        elif campaign_info.count() == 0:
            message = 'No campaign available.'
            logger.critical(message)
            raise RuntimeError(message)

        return campaign_info.first()

    def get_campaign_id(self, name):
        selected = self.session.query(
            CampaignTable.name.label(name),
            CampaignTable.id).all()
        if len(selected) == 0:
            msg = f"No campaign with name {name} found in campaign database"
            logger.error(msg)
            raise Exception(msg)
        if len(selected) > 1:
            msg = (
                f"More than one campaign with name {name} found in"
                f"campaign database. Database state is compromised."
            )
            logger.error(msg)
            raise Exception(msg)

        # Return the database ID for the specified campaign
        return selected[0][1]

    def campaign_dir(self, campaign_name=None):
        """Get campaign directory for `campaign_name`.

        Parameters
        ----------
        campaign_name: str
            Name of campaign to select

        Returns
        -------
        str:
            Path to campaign directory.
        """

        self._get_campaign_info(campaign_name=campaign_name).campaign_dir

    def runs(self, campaign=None, sampler=None):
        """
        Get a dictionary of all run information for selected `campaign` and
        `sampler`.

        Parameters
        ----------
        campaign: int
            Campaign id to filter for.
        sampler: int
            Sampler id to filter for.

        Returns
        -------
        dict:
            Information on all selected runs (key = run_name, value = dict of
            run information fields.).

        """
        # TODO: This is a bad idea - find a better generator solution

        if campaign is None and sampler is None:
            selected = self.session.query(RunTable).all()
        elif campaign is not None and sampler is not None:
            selected = self.session.query(RunTable).filter_by(
                campaign=campaign, sample=sampler).all()
        elif campaign is not None:
            selected = self.session.query(RunTable)
            selected = selected.filter_by(campaign=campaign).all()
        else:
            selected = self.session.query(
                RunTable).filter_by(sample=sampler).all()

        return {r.run_name: self._run_to_dict(r) for r in selected}

    def runs_dir(self, campaign_name=None):
        """
        Get the directory used to store run information for `campaign_name`.

        Parameters
        ----------
        campaign_name: str
            Name of the selected campaign.

        Returns
        -------
        str:
            Path containing run outputs.
        """

        return self._get_campaign_info(campaign_name=campaign_name).runs_dir

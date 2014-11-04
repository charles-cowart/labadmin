#!/usr/bin/env python
from tornado.web import authenticated
from knimin.handlers.base import BaseHandler

from amgut.util import AG_DATA_ACCESS


class AGEditBarcodeHandler(BaseHandler):
    @authenticated
    def get(self):
        barcode = self.get_argument('barcode', None)
        if barcode is not None:
            details = AG_DATA_ACCESS.getAGBarcodeDetails(barcode)
            site_sampled = AG_DATA_ACCESS.human_sites
            environment_sampled = AG_DATA_ACCESS.general_sites
            logins = AG_DATA_ACCESS.getAGKitsByLogin()
            self.render("ag_edit_barcode.html", response=None, barcode=barcode,
                        sites_sampled=site_sampled, details=details,
                        environments_sampled=environment_sampled,
                        logins=logins, currentuser=self.current_user)

    @authenticated
    def post(self):
        barcode = self.get_argument('barcode')
        ag_kit_id = self.get_argument('ag_kit_id')
        site_sampled = self.get_argument('site_sampled')
        environment_sampled = self.get_argument('environment_sampled')
        sample_date = self.get_argument('sample_date')
        sample_time = self.get_argument('sample_time')
        participant_name = self.get_argument('participant_name')
        notes = self.get_argument('notes')
        refunded = self.get_argument('refunded')
        withdrawn = self.get_argument('withdrawn')
        try:
            AG_DATA_ACCESS.updateAGBarcode(barcode, ag_kit_id, site_sampled,
                                           environment_sampled, sample_date,
                                           sample_time, participant_name,
                                           notes, refunded, withdrawn)
            self.render("ag_edit_barcode.html", response='Good', barcode=None,
                        sites_sampled=None, details=None,
                        environments_sampled=None,
                        logins=None, currentuser=self.current_user)
        except:
            self.render("ag_edit_barcode.html", response='Bad', barcode=None,
                        sites_sampled=None, details=None,
                        environments_sampled=None,
                        logins=None, currentuser=self.current_user)
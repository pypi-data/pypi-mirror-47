############################################################
# -*- coding: utf-8 -*-
#
# MOUNTCONTROL
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
############################################################
# standard libraries
import unittest
import unittest.mock as mock
import numpy
# external packages
import skyfield.api
# local imports
from mountcontrol.model import AlignStar
from mountcontrol.model import Model
from mountcontrol.model import APoint


class TestConfigData(unittest.TestCase):

    def setUp(self):
        pass

    #
    #
    # testing host
    #
    #

    def test_Model_host_ok1(self):
        model = Model()
        model.host = ('192.168.2.1', 1234)
        self.assertEqual(('192.168.2.1', 1234), model.host)

    def test_Model_host_ok2(self):
        model = Model()
        model.host = '192.168.2.1'
        self.assertEqual(('192.168.2.1', 3492), model.host)

    def test_Model_host_not_ok1(self):
        model = Model()
        model.host = ''
        self.assertEqual(None, model.host)

    def test_Model_host_not_ok2(self):
        model = Model()
        model.host = 2357
        self.assertEqual(None, model.host)

    #
    #
    # testing the class Model and it's attribute
    #
    #

    def test_Model_altitudeError(self):
        align = Model()
        align.altitudeError = '67'
        self.assertEqual(67, align.altitudeError.degrees)
        self.assertEqual(67, align._altitudeError.degrees)

    def test_Model_azimuthError(self):
        align = Model()
        align.azimuthError = '67'
        self.assertEqual(67, align.azimuthError.degrees)
        self.assertEqual(67, align._azimuthError.degrees)

    def test_Model_polarError(self):
        align = Model()
        align.polarError = '67'
        self.assertEqual(67, align.polarError.degrees)
        self.assertEqual(67, align._polarError.degrees)

    def test_Model_positionAngle1(self):
        align = Model()
        align.positionAngle = '67'
        self.assertEqual(67, align.positionAngle.degrees)
        self.assertEqual(67, align._positionAngle.degrees)

    def test_Model_positionAngle2(self):
        align = Model()
        align.positionAngle = skyfield.api.Angle(degrees=67)
        self.assertNotEqual(67, align.positionAngle)
        self.assertNotEqual(67, align._positionAngle)

    def test_Model_orthoError(self):
        align = Model()
        align.orthoError = '67'
        self.assertEqual(67, align.orthoError.degrees)
        self.assertEqual(67, align._orthoError.degrees)

    def test_Model_altitudeTurns(self):
        align = Model()
        align.altitudeTurns = '67'
        self.assertEqual(67, align.altitudeTurns)
        self.assertEqual(67, align._altitudeTurns)

    def test_Model_azimuthTurns(self):
        align = Model()
        align.azimuthTurns = '67'
        self.assertEqual(67, align.azimuthTurns)
        self.assertEqual(67, align._azimuthTurns)

    def test_Model_terms(self):
        align = Model()
        align.terms = '67'
        self.assertEqual(67, align.terms)
        self.assertEqual(67, align._terms)

    def test_Model_errorRMS(self):
        align = Model()
        align.errorRMS = '67'
        self.assertEqual(67, align.errorRMS)
        self.assertEqual(67, align._errorRMS)

    def test_Model_numberStars(self):
        align = Model()
        align.numberStars = '67'
        self.assertEqual(67, align.numberStars)
        self.assertEqual(67, align._numberStars)

    def test_Model_numberNames(self):
        align = Model()
        align.numberNames = '67'
        self.assertEqual(67, align.numberNames)
        self.assertEqual(67, align._numberNames)

    def test_Model_starList1(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        p4 = '90'
        modelStar1 = AlignStar(coord=(p1, p2), errorRMS=p3, errorAngle=p4, number=1)

        model = Model()

        self.assertEqual(len(model.starList), 0)
        model.starList = [modelStar1]
        self.assertEqual(len(model.starList), 1)

    def test_Model_starList2(self):
        model = Model()

        self.assertEqual(len(model.starList), 0)
        model.starList = '67'
        self.assertEqual(len(model.starList), 0)

    def test_Model_starList3(self):
        model = Model()

        self.assertEqual(len(model.starList), 0)
        model.starList = ['67', '78']
        self.assertEqual(len(model.starList), 0)

    def test_add_del_Star(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        p4 = '90'
        modelStar1 = AlignStar(coord=(p1, p2), errorRMS=p3, errorAngle=p4, number=1)
        modelStar2 = AlignStar(coord=(p1, p2), errorRMS=p3, errorAngle=p4, number=2)
        modelStar3 = AlignStar(coord=(p1, p2), errorRMS=p3, errorAngle=p4, number=3)
        modelStar4 = AlignStar(coord=(p1, p2), errorRMS=p3, errorAngle=p4, number=4)

        model = Model()

        self.assertEqual(len(model.starList), 0)
        model.addStar(modelStar1)
        self.assertEqual(len(model.starList), 1)
        model.addStar(modelStar2)
        self.assertEqual(len(model.starList), 2)
        model.addStar(modelStar3)
        self.assertEqual(len(model.starList), 3)
        model.addStar(modelStar4)
        self.assertEqual(len(model.starList), 4)
        model.delStar(3)
        self.assertEqual(len(model.starList), 3)
        model.delStar(3)
        self.assertEqual(len(model.starList), 3)
        model.delStar(-1)
        self.assertEqual(len(model.starList), 3)
        model.delStar(1)
        self.assertEqual(len(model.starList), 2)

    def test_addStar_ok(self):
        model = Model()
        self.assertEqual(len(model.starList), 0)
        model.addStar('12:45:33.01,+56*30:00.5,1234.5,90,1')
        self.assertEqual(len(model.starList), 1)

    def test_addStar_not_ok1(self):
        model = Model()

        self.assertEqual(len(model.starList), 0)
        model.addStar(67)
        self.assertEqual(len(model.starList), 0)

    def test_addStar_not_ok2(self):
        model = Model()

        self.assertEqual(len(model.starList), 0)
        model.addStar('test')
        self.assertEqual(len(model.starList), 0)

    def test_StarList_iteration(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        model = Model()

        for i in range(0, 10):
            model.addStar(AlignStar(coord=(p1, p2),
                                    errorRMS=str(i*i),
                                    errorAngle=str(i*i),
                                    number=str(i)))

        self.assertEqual(len(model.starList), 10)
        for i, star in enumerate(model.starList):
            self.assertEqual(i,
                             star.number)
            self.assertEqual(i*i,
                             star.errorRMS)

    def test_StarList_checkStarListOK(self):
        model = Model()
        self.assertEqual(len(model.starList), 0)
        model.addStar('12:45:33.01,+56*30:00.5,1234.5,90,1')
        model.numberStars = 1
        self.assertEqual(True, model.checkStarListOK())

    def test_StarList_checkStarList_not_OK1(self):
        model = Model()
        self.assertEqual(len(model.starList), 0)
        model.addStar('12:45:33.01,+56*30:00.5,1234.5,90,1')
        model.numberStars = 2
        self.assertEqual(False, model.checkStarListOK())

    def test_StarList_checkStarList_not_OK2(self):
        model = Model()
        self.assertEqual(len(model.starList), 0)
        model.addStar('12:45:33.01,+56*30:00.5,1234.5,90,1')
        self.assertEqual(False, model.checkStarListOK())

    def test_Model_nameList1(self):

        model = Model()

        self.assertEqual(len(model.nameList), 0)
        model.nameList = 67
        self.assertEqual(len(model.nameList), 0)

    def test_Model_nameList2(self):
        model = Model()

        self.assertEqual(len(model.nameList), 0)
        model.nameList = ['67']
        self.assertEqual(len(model.nameList), 1)

    def test_Model_nameList3(self):
        model = Model()

        self.assertEqual(len(model.nameList), 0)
        model.nameList = ['67', '78']
        self.assertEqual(len(model.nameList), 2)

    def test_Model_nameList4(self):
        model = Model()

        self.assertEqual(len(model.nameList), 0)
        model.nameList = ['67', 67]
        self.assertEqual(len(model.nameList), 0)

    def test_add_del_Name(self):
        model = Model()

        self.assertEqual(len(model.nameList), 0)
        model.addName('the first one')
        self.assertEqual(len(model.nameList), 1)
        model.addName('the second one')
        self.assertEqual(len(model.nameList), 2)
        model.addName('the third one')
        self.assertEqual(len(model.nameList), 3)
        model.addName('the fourth one')
        self.assertEqual(len(model.nameList), 4)
        model.delName(3)
        self.assertEqual(len(model.nameList), 3)
        model.delName(3)
        self.assertEqual(len(model.nameList), 3)
        model.delName(-1)
        self.assertEqual(len(model.nameList), 3)
        model.delName(1)
        self.assertEqual(len(model.nameList), 2)

    def test_addName_not_ok(self):
        model = Model()

        self.assertEqual(len(model.nameList), 0)
        model.addName(45)
        self.assertEqual(len(model.nameList), 0)

    def test_NameList_iteration(self):
        model = Model()

        for i in range(0, 10):
            model.addName('this is the {0}.th name'.format(i))
        self.assertEqual(len(model.nameList), 10)
        for i, name in enumerate(model.nameList):
            self.assertEqual('this is the {0}.th name'.format(i),
                             name)

    def test_StarList_checkNameListOK(self):
        model = Model()
        self.assertEqual(len(model.starList), 0)
        model.addName('12:45:33.01,+56*30:00.5,1234.5,90,1')
        model.numberNames = 1
        self.assertEqual(True, model.checkNameListOK())

    def test_StarList_checkNameList_not_OK1(self):
        model = Model()
        self.assertEqual(len(model.starList), 0)
        model.addName('12:45:33.01,+56*30:00.5,1234.5,90,1')
        model.numberNames = 2
        self.assertEqual(False, model.checkNameListOK())

    def test_StarList_checkNameList_not_OK2(self):
        model = Model()
        self.assertEqual(len(model.starList), 0)
        model.addName('12:45:33.01,+56*30:00.5,1234.5,90,1')
        self.assertEqual(False, model.checkNameListOK())
    #
    #
    # testing the specific QCI behaviour in Model class attributes
    #
    #

    def test_errorRMS_HPS(self):
        model = Model()
        model.errorRMS = '36.8'
        self.assertEqual(36.8, model.errorRMS)
        self.assertEqual(36.8, model._errorRMS)

    def test_errorRMS_HPS_empty(self):
        model = Model()
        model.errorRMS = 'E'
        self.assertEqual(None, model.errorRMS)

    def test_errorRMS_HPS_float(self):
        model = Model()
        model.errorRMS = 36.8
        self.assertEqual(36.8, model.errorRMS)

    def test_errorRMS_HPS_int(self):
        model = Model()
        model.errorRMS = 36
        self.assertEqual(36.0, model.errorRMS)

    def test_errorRMS_HPS_tuple(self):
        model = Model()
        model.errorRMS = (36.8, 1.0)
        self.assertEqual(None, model.errorRMS)

    def test_errorRMS_QCI(self):
        model = Model()
        model.errorRMS = ''
        self.assertEqual(None, model.errorRMS)

    def test_errorTerms_QCI(self):
        model = Model()
        model.terms = ''
        self.assertEqual(None, model.terms)

    #
    #
    # testing workaround
    #
    #

    def test_parseWorkaround_ok(self):
        model = Model()
        response = ['V', 'E']
        suc = model._parseWorkaround(response, 2)
        self.assertEqual(True, suc)

    def test_parseWorkaround_not_ok1(self):
        model = Model()
        response = ['V']
        suc = model._parseWorkaround(response, 2)
        self.assertEqual(False, suc)

    def test_parseWorkaround_not_ok2(self):
        model = Model()
        response = ['V', 'V']
        suc = model._parseWorkaround(response, 2)
        self.assertEqual(False, suc)

    def test_parseWorkaround_not_ok3(self):
        model = Model()
        response = ['E', 'E']
        suc = model._parseWorkaround(response, 2)
        self.assertEqual(False, suc)

    def test_workaroundAlign_ok(self):
        model = Model()

        response = ['V', 'E']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.workaroundAlign()
            self.assertEqual(True, suc)

    def test_workaroundAlign_not_ok(self):
        model = Model()

        response = ['V', 'E']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 2
            suc = model.workaroundAlign()
            self.assertEqual(False, suc)

    #
    #
    # testing the class AlignStar and it's attribute setters
    #
    #

    def test_AlignStar_coord1(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        p4 = '90'
        alignStar = AlignStar(coord=(p1, p2), errorRMS=p3, errorAngle=p4, number=1)
        self.assertAlmostEqual(alignStar.coord.ra.hms()[0], 12, 6)
        self.assertAlmostEqual(alignStar.coord.ra.hms()[1], 45, 6)
        self.assertAlmostEqual(alignStar.coord.ra.hms()[2], 33.01, 6)
        self.assertAlmostEqual(alignStar.coord.dec.dms()[0], 56, 6)
        self.assertAlmostEqual(alignStar.coord.dec.dms()[1], 30, 6)
        self.assertAlmostEqual(alignStar.coord.dec.dms()[2], 0.5, 6)

    def test_AlignStar_coord2(self):
        star = skyfield.api.Star(ra_hours=12.55, dec_degrees=56.55)
        p3 = '1234.5'
        p4 = '90'
        alignStar = AlignStar(coord=star, errorRMS=p3, errorAngle=p4, number=1)
        self.assertAlmostEqual(alignStar.coord.ra.hms()[0], 12, 6)
        self.assertAlmostEqual(alignStar.coord.ra.hms()[1], 33, 6)
        self.assertAlmostEqual(alignStar.coord.ra.hms()[2], 0, 6)
        self.assertAlmostEqual(alignStar.coord.dec.dms()[0], 56, 6)
        self.assertAlmostEqual(alignStar.coord.dec.dms()[1], 33, 6)
        self.assertAlmostEqual(alignStar.coord.dec.dms()[2], 0, 6)

    def test_AlignStar_coord_not_ok1(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        alignStar = AlignStar(coord=(p1, p2, p3))
        self.assertEqual(None, alignStar.coord)

    def test_AlignStar_coord_not_ok2(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        alignStar = AlignStar(coord=[p1, p2, p3])
        self.assertEqual(None, alignStar.coord)

    def test_AlignStar_coord_not_ok3(self):
        alignStar = AlignStar(coord=56)
        self.assertEqual(None, alignStar.coord)

    def test_AlignStar_coord_not_ok4(self):
        p1 = '12:45:33.01'
        alignStar = AlignStar(coord=(p1, 67))
        self.assertEqual(None, alignStar.coord)

    def test_AlignStar_number(self):
        alignStar = AlignStar()
        alignStar.number = 6
        self.assertEqual(6, alignStar.number)

    def test_AlignStar_number1(self):
        alignStar = AlignStar()
        alignStar.number = '6'
        self.assertEqual(6, alignStar.number)

    def test_AlignStar_errorAngle(self):
        alignStar = AlignStar()
        alignStar.errorAngle = 50
        self.assertEqual(50, alignStar.errorAngle.degrees)

    def test_AlignStar_errorRMS(self):
        alignStar = AlignStar()
        alignStar.errorRMS = 6
        self.assertEqual(6, alignStar.errorRMS)

    def test_AlignStar_error_DEC_RA(self):
        alignStar = AlignStar()
        alignStar.errorRMS = 6
        alignStar.errorAngle = 50
        ra = 6 * numpy.sin(50 * numpy.pi * 2 / 360)
        dec = 6 * numpy.cos(50 * numpy.pi * 2 / 360)
        self.assertAlmostEqual(ra, alignStar.errorRA())
        self.assertAlmostEqual(dec, alignStar.errorDEC())

    #
    #
    # testing the conversion functions
    #
    #

    def test_APoint_mCoord1(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        aPoint = APoint(mCoord=(p1, p2),
                        pierside='W',
                        sCoord=(p1, p2),
                        sidereal=p1,
                        )
        self.assertAlmostEqual(aPoint.mCoord.ra.hms()[0], 12, 6)
        self.assertAlmostEqual(aPoint.mCoord.ra.hms()[1], 45, 6)
        self.assertAlmostEqual(aPoint.mCoord.ra.hms()[2], 33.01, 6)
        self.assertAlmostEqual(aPoint.mCoord.dec.dms()[0], 56, 6)
        self.assertAlmostEqual(aPoint.mCoord.dec.dms()[1], 30, 6)
        self.assertAlmostEqual(aPoint.mCoord.dec.dms()[2], 0.5, 6)

        self.assertAlmostEqual(aPoint.sCoord.ra.hms()[0], 12, 6)
        self.assertAlmostEqual(aPoint.sCoord.ra.hms()[1], 45, 6)
        self.assertAlmostEqual(aPoint.sCoord.ra.hms()[2], 33.01, 6)
        self.assertAlmostEqual(aPoint.sCoord.dec.dms()[0], 56, 6)
        self.assertAlmostEqual(aPoint.sCoord.dec.dms()[1], 30, 6)
        self.assertAlmostEqual(aPoint.sCoord.dec.dms()[2], 0.5, 6)

    def test_APoint_mCoord2(self):
        p1 = '12:45:33.01'
        star = skyfield.api.Star(ra_hours=12.55, dec_degrees=56.55)
        aPoint = APoint(mCoord=star,
                        pierside='W',
                        sCoord=star,
                        sidereal=p1,
                        )
        self.assertAlmostEqual(aPoint.mCoord.ra.hms()[0], 12, 6)
        self.assertAlmostEqual(aPoint.mCoord.ra.hms()[1], 33, 6)
        self.assertAlmostEqual(aPoint.mCoord.ra.hms()[2], 0, 6)
        self.assertAlmostEqual(aPoint.mCoord.dec.dms()[0], 56, 6)
        self.assertAlmostEqual(aPoint.mCoord.dec.dms()[1], 33, 6)
        self.assertAlmostEqual(aPoint.mCoord.dec.dms()[2], 0, 6)

        self.assertAlmostEqual(aPoint.sCoord.ra.hms()[0], 12, 6)
        self.assertAlmostEqual(aPoint.sCoord.ra.hms()[1], 33, 6)
        self.assertAlmostEqual(aPoint.sCoord.ra.hms()[2], 0, 6)
        self.assertAlmostEqual(aPoint.sCoord.dec.dms()[0], 56, 6)
        self.assertAlmostEqual(aPoint.sCoord.dec.dms()[1], 33, 6)
        self.assertAlmostEqual(aPoint.sCoord.dec.dms()[2], 0, 6)

    def test_APoint_mCoord_not_ok1(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        aPoint = APoint(mCoord=(p1, p2, p3))
        self.assertEqual(None, aPoint.mCoord)

    def test_APoint_mCoord_not_ok2(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        aPoint = APoint(mCoord=[p1, p2, p3])
        self.assertEqual(None, aPoint.mCoord)

    def test_APoint_mCoord_not_ok3(self):
        aPoint = APoint(mCoord=56)
        self.assertEqual(None, aPoint.mCoord)

    def test_APoint_mCoord_not_ok4(self):
        p1 = '12:45:33.01'
        aPoint = APoint(mCoord=(p1, 67))
        self.assertEqual(None, aPoint.mCoord)

    def test_APoint_sCoord_not_ok1(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        aPoint = APoint(sCoord=(p1, p2, p3))
        self.assertEqual(None, aPoint.sCoord)

    def test_APoint_sCoord_not_ok2(self):
        p1 = '12:45:33.01'
        p2 = '+56*30:00.5'
        p3 = '1234.5'
        aPoint = APoint(sCoord=[p1, p2, p3])
        self.assertEqual(None, aPoint.sCoord)

    def test_APoint_sCoord_not_ok3(self):
        aPoint = APoint(sCoord=56)
        self.assertEqual(None, aPoint.sCoord)

    def test_APoint_sCoord_not_ok4(self):
        p1 = '12:45:33.01'
        aPoint = APoint(sCoord=(p1, 67))
        self.assertEqual(None, aPoint.sCoord)

    def test_APoint_pierside(self):
        aPoint = APoint()
        aPoint.pierside = 'E'
        self.assertEqual('E', aPoint.pierside)

    def test_APoint_sidereal(self):
        aPoint = APoint()
        aPoint.sidereal = 'E'
        self.assertEqual('E', aPoint.sidereal)

    def test_Model_parseNumberName_ok(self):
        model = Model()
        response = ['5']
        suc = model._parseNumberNames(response, 1)
        self.assertEqual(True, suc)

    def test_Model_parseNumberName_not_ok1(self):
        model = Model()
        response = ['df']
        suc = model._parseNumberNames(response, 1)
        self.assertEqual(True, suc)

    def test_Model_parseNumberName_not_ok2(self):
        model = Model()
        response = ['']
        suc = model._parseNumberNames(response, 1)
        self.assertEqual(True, suc)

    def test_Model_parseNumberName_not_ok3(self):
        model = Model()
        response = ['5a']
        suc = model._parseNumberNames(response, 1)
        self.assertEqual(True, suc)

    def test_Model_parseNumberName_not_ok4(self):
        model = Model()
        response = ['5', '4']
        suc = model._parseNumberNames(response, 1)
        self.assertEqual(False, suc)

    def test_Model_parseNumberName_not_ok5(self):
        model = Model()
        response = ['5', 'g']
        suc = model._parseNumberNames(response, 1)
        self.assertEqual(False, suc)
    #
    #
    # testing modelNames
    #
    #

    def test_Model_parseNames_ok1(self):
        model = Model()
        response = ['test']
        suc = model._parseNames(response, 1)
        self.assertEqual(True, suc)

    def test_Model_parseNames_ok2(self):
        model = Model()
        response = ['sd', '', None]
        suc = model._parseNames(response, 3)
        self.assertEqual(True, suc)

    def test_Model_parseNumberNames_ok3(self):
        model = Model()
        response = ['5']
        suc = model._parseNumberNames(response, 1)
        self.assertEqual(True, suc)

    def test_Model_parseNames_not_ok1(self):
        model = Model()
        response = ['sd']
        suc = model._parseNames(response, 3)
        self.assertEqual(False, suc)

    def test_Model_parseNumberNames_not_ok2(self):
        model = Model()
        response = ['sd']
        suc = model._parseNumberNames(response, 1)
        self.assertEqual(True, suc)

    def test_Model_parseNumberNames_not_ok3(self):
        model = Model()
        response = ['5', '6']
        suc = model._parseNumberNames(response, 2)
        self.assertEqual(False, suc)

    def test_Model_pollNames_ok(self):
        model = Model()

        response = ['100']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.pollNames()
            self.assertEqual(True, suc)

    def test_Model_pollNames_not_ok1(self):
        model = Model()

        response = ['100']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 1
            suc = model.pollNames()
            self.assertEqual(False, suc)

    def test_Model_pollNames_not_ok2(self):
        model = Model()

        response = ['100']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 6
            suc = model.pollNames()
            self.assertEqual(False, suc)

    #
    #
    # testing model stars
    #
    #

    def test_Model_parseNumberStars_ok1(self):
        model = Model()
        response = ['0', 'E']
        suc = model._parseNumberStars(response, 2)
        self.assertEqual(True, suc)

    def test_Model_parseNumberStars_ok2(self):
        model = Model()
        response = \
            ['1', '023.8311, +24.8157, 29.8580, 227.45, -12.9985, +26.98, -08.97, 11, 97751.6']
        suc = model._parseNumberStars(response, 2)
        self.assertEqual(True, suc)

    def test_Model_parseNumberStars_not_ok0(self):
        model = Model()
        response = ['4', 'E']
        suc = model._parseNumberStars(response, 1)
        self.assertEqual(False, suc)

    def test_Model_parseNumberStars_not_ok1(self):
        model = Model()
        response = ['4']
        suc = model._parseNumberStars(response, 1)
        self.assertEqual(False, suc)

    def test_Model_parseNumberStars_not_ok2(self):
        model = Model()
        response = ['4', '4, 4, 4']
        suc = model._parseNumberStars(response, 2)
        self.assertEqual(False, suc)

    def test_Model_parseNumberStars_not_ok3(self):
        model = Model()
        response = ['4', '4']
        suc = model._parseNumberStars(response, 2)
        self.assertEqual(False, suc)

    def test_Model_parseStars_ok(self):
        model = Model()
        response = [
            '21:52:58.95,+08*56:10.1,   5.7,201',
            '21:06:10.79,+45*20:52.8,  12.1,329',
            '23:13:58.02,+38*48:18.8,  31.0,162',
            '17:43:41.26,+59*15:30.7,   8.4,005',
            '20:36:01.52,+62*39:32.4,  19.5,138',
            '03:43:11.04,+19*06:30.3,  22.6,199',
            '05:03:10.81,+38*14:22.2,  20.1,340',
            '04:12:55.39,+49*14:00.2,  17.1,119',
            '06:57:55.11,+61*40:26.8,   9.8,038',
            '22:32:24.00,+28*00:23.6,  42.1,347',
            '13:09:03.49,+66*24:40.5,  13.9,177',
        ]
        suc = model._parseStars(response, 11)
        self.assertEqual(True, suc)
        self.assertEqual(len(model.starList), 11)

    def test_Model_parseStars_not_ok1(self):
        model = Model()
        response = [
            '21:52:58.95,+08*56:10.1,   5.7,201',
            '21:06:10.79,+45*20:52.8,  12.1,329',
            '23:13:58.02,+38*48:18.8,  31.0,162',
            '06:57:55.11,+61*40:26.8,   9.8,038',
            '22:32:24.00,+28*00:23.6,  42.1,347',
            '13:09:03.49,+66*24:40.5,  13.9,177',
        ]
        suc = model._parseStars(response, 4)
        self.assertEqual(False, suc)
        self.assertEqual(len(model.starList), 0)

    def test_Model_parseStars_not_ok2(self):
        model = Model()
        response = [
            '21:52:58.95,+08*56:10.1,   5.7,201',
            ''
        ]
        suc = model._parseStars(response, 2)
        self.assertEqual(True, suc)
        self.assertEqual(len(model.starList), 1)

    def test_Model_pollStars_ok1(self):
        model = Model()

        response = ['100']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.pollStars()
            self.assertEqual(False, suc)

    def test_Model_pollStars_ok2(self):
        model = Model()

        response = []
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 0
            suc = model.pollStars()
            self.assertEqual(False, suc)

    def test_Model_pollStars_not_ok1(self):
        model = Model()

        response = ['100', '']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 2
            suc = model.pollStars()
            self.assertEqual(False, suc)

    def test_Model_pollStars_not_ok2(self):
        model = Model()

        response = ['100']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 6
            suc = model.pollStars()
            self.assertEqual(False, suc)
    #
    #
    # testing pollCount
    #
    #

    def test_Model_pollCount_ok(self):
        model = Model()
        response = ['5', '6']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.pollCount()
            self.assertEqual(True, suc)
            self.assertEqual(5, model.numberNames)
            self.assertEqual(6, model.numberStars)

    def test_Model_pollCount_not_ok1(self):
        model = Model()
        response = ['', '45']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.pollCount()
            self.assertEqual(True, suc)
            self.assertEqual(None, model.numberNames)
            self.assertEqual(45, model.numberStars)

    def test_Model_pollCount_not_ok2(self):
        model = Model()
        response = ['']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.pollCount()
            self.assertEqual(False, suc)
            self.assertEqual(None, model.numberNames)
            self.assertEqual(None, model.numberStars)

    def test_Model_pollCount_not_ok3(self):
        model = Model()
        response = ['4t']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.pollCount()
            self.assertEqual(False, suc)
            self.assertEqual(None, model.numberNames)
            self.assertEqual(None, model.numberStars)

    def test_Model_pollCount_not_ok4(self):
        model = Model()
        response = ['4', '5', '5']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.pollCount()
            self.assertEqual(False, suc)
            self.assertEqual(None, model.numberNames)
            self.assertEqual(None, model.numberStars)

    def test_Model_pollCount_not_ok5(self):
        model = Model()
        response = ['4', 'r']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.pollCount()
            self.assertEqual(True, suc)
            self.assertEqual(4, model.numberNames)
            self.assertEqual(None, model.numberStars)

    #
    #
    # testing clearAlign
    #
    #

    def test_Model_clearAlign_ok(self):
        model = Model()

        response = ['']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.clearAlign()
            self.assertEqual(True, suc)

    def test_Model_clearAlign_not_ok1(self):
        model = Model()

        response = ['']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 1
            suc = model.clearAlign()
            self.assertEqual(False, suc)

    def test_Model_clearAlign_not_ok2(self):
        model = Model()

        response = [' ']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.clearAlign()
            self.assertEqual(False, suc)

    #
    #
    # testing deletePoint
    #
    #

    def test_Model_deletePoint_ok(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.deletePoint(1)
            self.assertEqual(True, suc)

    def test_Model_deletePoint_not_ok1(self):
        model = Model()

        response = ['1#']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 1
            suc = model.deletePoint(1)
            self.assertEqual(False, suc)

    def test_Model_deletePoint_not_ok2(self):
        model = Model()

        response = ['0#']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.deletePoint(1)
            self.assertEqual(False, suc)

    def test_Model_deletePoint_not_ok3(self):
        model = Model()

        response = ['0#']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.deletePoint('1')
            self.assertEqual(False, suc)

    #
    #
    # testing storeName
    #
    #

    def test_Model_storeName_ok1(self):
        model = Model()

        response = ['1', '1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.storeName('test')
            self.assertEqual(True, suc)

    def test_Model_storeName_ok2(self):
        model = Model()

        response = ['0', '1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.storeName('Test')
            self.assertEqual(True, suc)

    def test_Model_storeName_not_ok1(self):
        model = Model()

        response = ['1', '0']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.storeName('test')
            self.assertEqual(False, suc)

    def test_Model_storeName_not_ok2(self):
        model = Model()

        response = ['1', '1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 2
            suc = model.storeName('test')
            self.assertEqual(False, suc)

    def test_Model_storeName_not_ok3(self):
        model = Model()

        response = ['1', '1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.storeName('1234567890123456')
            self.assertEqual(False, suc)

    def test_Model_storeName_not_ok4(self):
        model = Model()

        response = ['0', '1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 2
            suc = model.storeName(2423487)
            self.assertEqual(False, suc)

    #
    #
    # testing loadName
    #
    #

    def test_Model_loadName_ok(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.loadName('test')
            self.assertEqual(True, suc)

    def test_Model_loadName_not_ok1(self):
        model = Model()

        response = ['0']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.loadName('test')
            self.assertEqual(False, suc)

    def test_Model_loadName_not_ok2(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 1
            suc = model.loadName('test')
            self.assertEqual(False, suc)

    def test_Model_loadName_not_ok3(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.loadName('1234567890123456')
            self.assertEqual(False, suc)

    def test_Model_loadName_not_ok4(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.loadName(3567)
            self.assertEqual(False, suc)

    #
    #
    # testing deleteName
    #
    #

    def test_Model_deleteName_ok(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.deleteName('test')
            self.assertEqual(True, suc)

    def test_Model_deleteName_not_ok1(self):
        model = Model()

        response = ['0']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.deleteName('test')
            self.assertEqual(False, suc)

    def test_Model_deleteName_not_ok2(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = False, response, 1
            suc = model.deleteName('test')
            self.assertEqual(False, suc)

    def test_Model_deleteName_not_ok3(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.deleteName('1234567890123456')
            self.assertEqual(False, suc)

    def test_Model_deleteName_not_ok4(self):
        model = Model()

        response = ['1']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, response, 1
            suc = model.deleteName(3567)
            self.assertEqual(False, suc)

    #
    #
    # testing programAlign
    #
    #

    def test_Model_programAlign_ok1(self):
        model = Model()

        aPoint = APoint()
        build = [aPoint]
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, ['1'], 1
            suc = model.programAlign(build)
            self.assertEqual(True, suc)

    def test_Model_programAlign_ok2(self):
        model = Model()

        aPoint = APoint()
        build = [aPoint]
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, ['1'], 1
            suc = model.programAlign(build)
            self.assertEqual(True, suc)
            mConn.return_value.communicate.assert_called_with(':newalig#:endalig#')

    def test_Model_programAlign_ok3(self):
        model = Model()
        v1 = ':newalig#:newalpt19:35:15.6,-15*02:043,W,19:35:45.3,-15*03:042,17:35:31.75#:endalig#'

        build = self.gatherData(1)
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, ['E'], 1
            suc = model.programAlign(build)
            self.assertEqual(False, suc)
            mConn.return_value.communicate.assert_called_with(v1)

    def test_Model_programAlign_not_ok1(self):
        model = Model()

        aPoint = APoint()
        build = [aPoint]
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, ['E'], 1
            suc = model.programAlign(build)
            self.assertEqual(False, suc)

    def test_Model_programAlign_not_ok2(self):
        model = Model()

        aPoint = APoint()
        build = [aPoint, 'test']
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, ['E'], 1
            suc = model.programAlign(build)
            self.assertEqual(False, suc)

    def test_Model_programAlign_not_ok3(self):
        model = Model()

        aPoint = APoint()
        build = [aPoint]
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, ['E'], 1
            suc = model.programAlign(build)
            self.assertEqual(False, suc)

    def test_Model_programAlign_not_ok4(self):
        model = Model()

        build = 'Test'
        with mock.patch('mountcontrol.model.Connection') as mConn:
            mConn.return_value.communicate.return_value = True, ['E'], 1
            suc = model.programAlign(build)
            self.assertEqual(False, suc)

    @staticmethod
    def gatherData(number):
        import json
        with open('./mountcontrol/test/2018-07-08-21-41-44_full.dat', 'r') as infile:
            data = json.load(infile)

        maxNum = len(data['Index'])
        if number > maxNum:
            number = maxNum
        build = []
        for i in range(0, number):
            aPoint = APoint()
            aPoint.mCoord = skyfield.api.Star(ra_hours=data['RaJNow'][i],
                                              dec_degrees=data['DecJNow'][i])
            aPoint.sCoord = skyfield.api.Star(ra_hours=data['RaJNowSolved'][i],
                                              dec_degrees=data['DecJNowSolved'][i])
            aPoint.pierside = data['Pierside'][i]
            aPoint.sidereal = data['LocalSiderealTime'][i]
            build.append(aPoint)
        build.append(APoint())
        return build

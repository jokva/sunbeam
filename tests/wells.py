import unittest
import sunbeam

spe3 = sunbeam.parse('spe3/SPE3CASE1.DATA')

class TestWells(unittest.TestCase):
    def setUp(self):
        self.wells = spe3.schedule.wells

    def inje(self):
        return next(iter(filter(sunbeam.Well.injector(0), self.wells)))

    def prod(self):
        return next(iter(filter(sunbeam.Well.producer(0), self.wells)))

    def testWellPos0(self):
        well = self.wells[0]
        i, j, refdepth = well.pos(0)

        self.assertEqual(6, i)
        self.assertEqual(6, j)
        self.assertEqual(2247.9, refdepth)

    def testWellProperty(self):
        well = self.wells[0]
        i, j, refdepth = well.pos()

        self.assertEqual(6, i)
        self.assertEqual(6, j)
        self.assertEqual(2247.9, refdepth)

    def testWellStatus(self):
        for well in self.wells:
            self.assertEqual("OPEN", well.status(0))

    def testGroupName(self):
        for well in self.wells:
            self.assertEqual("G1", well.group(0))

    def testPreferredPhase(self):
        inje, prod = self.inje(), self.prod()
        self.assertEqual("GAS", inje.preferred_phase)
        self.assertEqual("GAS", prod.preferred_phase)

    def testGuideRate(self):
        inje, prod = self.inje(), self.prod()
        self.assertEqual(-1.0, inje.guide_rate(1))
        self.assertEqual(-1.0, prod.guide_rate(1))

        self.assertEqual(-1.0, inje.guide_rate(14))
        self.assertEqual(-1.0, prod.guide_rate(14))

    def testGroupControl(self):
        inje, prod = self.inje(), self.prod()
        self.assertTrue(inje.available_gctrl(1))
        self.assertTrue(prod.available_gctrl(1))

        self.assertTrue(inje.available_gctrl(14))
        self.assertTrue(prod.available_gctrl(14))

    def testWellDefinedFilter(self):
        defined0 = filter(sunbeam.Well.defined(0), self.wells)
        defined1 = filter(sunbeam.Well.defined(1), self.wells)
        self.assertEqual(len(list(defined0)), 2)
        self.assertEqual(len(list(defined1)), 2)

    def testWellProdInjeFilter(self):
        inje = list(filter(sunbeam.Well.injector(0), self.wells))
        prod = list(filter(sunbeam.Well.producer(0), self.wells))

        self.assertEqual(len(inje), 1)
        self.assertEqual(len(prod), 1)

        self.assertEqual(inje[0].name, "INJ")
        self.assertEqual(prod[0].name, "PROD")

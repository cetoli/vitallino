"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/02/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.3 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: 2011, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.3 $Revision$"[10:-1]
__date__    = "2014/02/06 $Date$"
"""
from builder import Builder
from kwarwp_factory import Sprite, GUI
SIMPLE = ('..$$$&.!*' + '.' * 10 + ('\n' + '.' * 19) * 12)
#p = [['%s%d%d'%(p,x,y) for x, p in enumerate(' %s '%row)] for y, row in enumerate(border)]
#ES,FS = NullSprite, Sprite


def solver(a):
    a.go_left()
    a.go_left()
    a.go_take()
    a.go_give()


def main(pn, gui, spr=None, plan=SIMPLE, solver=solver):
    _builder = Builder()
    return _builder.build(pn, gui, _builder.build_inventory(FS=spr), plan, solver)


def web_main(dc, pn, gui=None, spr=None, plan=SIMPLE, solver=solver):
    #from kwarwp_factory import Sprite
    gui = GUI(dc['panel'], dc['data'], gui)
    _builder = Builder()
    place = _builder.build(
        pn, gui, _builder.build_inventory(FS=Sprite), plan, solver)

    dc['for'].addEventListener("click", place.actor.go_forward)
    dc['lef'].addEventListener("click", place.actor.go_left)
    dc['rig'].addEventListener("click", place.actor.go_right)
    dc['aft'].addEventListener("click", place.actor.go_backward)
    dc['tri'].addEventListener("click", place.actor.go_push)
    dc['exi'].addEventListener("click", place.actor.go_pull)
    dc['cir'].addEventListener("click", place.actor.go_take)
    dc['squ'].addEventListener("click", place.actor.go_give)
    dc['start'].addEventListener("click", place.actor.go_step)
    return place
#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pygame Factory : Gui interface to pygame
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/02/02  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2013/02/02 $Date$"

        
import mocker
from mocker import Mocker,KWARGS, ARGS, ANY, CONTAINS, MATCH, expect
#from kwarwp import Place,Way,Border,Door,Tar,Trunk
from main import main
from elements import *
from parts import *

class TestMain(mocker.MockerTestCase):
  """Testes unitários para o Pyjamas"""
  def __list(self):
        #INVENTORY = {'.':Way, ' ': Border, '&':Door, '@':Tar, '%':Border}
        ES =FS = self.mg       
        INVENTORY = {'.':[Way,ES,None], ' ': [Border,ES,None], '&':[Door,ES,None]
            , '@':[Tar,FS,'piche.gif'], '$':[Trunk,FS,'tronco.gif']}
        return INVENTORY

  def setUp(self):
    self.mock_gui = Mocker()
    self.mock_avt = Mocker()
    self.mg = self.mock_gui.mock()
    self.ma = self.mock_gui.mock()

  def tearDown(self):
    self.mock_gui.restore()
    self.mock_avt.restore()
    self.mock_avt.verify()
    self.mock_avt = None
    self.app = None
    pass

  def _expect_all_place(self):
    "place expectations"
    expect(self.mg.avatar()).result(self.ma)
    expect(self.mg.handler(ARGS)).count(1,6)
    expect(self.mg.rect(ARGS,KWARGS)).count(1,6)
    expect(self.mg.text(ARGS,KWARGS)).count(1,6)
    expect(self.ma.move(ARGS))
    expect(self.mg(ARGS)).count(1,96).result(self.ma)
  def _check_after_push(self,A,B):
    assert isinstance(self.app.plan[1][A], Way),self.app.plan[1][A]
    assert isinstance(self.app.plan[1][A].place, Place),self.app.plan[1][A].place
    assert isinstance(self.app.plan[1][A].thing, Trunk),self.app.plan[1][A].thing
    assert isinstance(self.app.plan[1][A].thing.place, Way),self.app.plan[1][B].thing.place
    assert self.app.plan[1][A].thing.place.x==A,self.app.plan[1][A].thing.place.x
    assert self.app.plan[1][A].thing.x==A,self.app.plan[1][A].thing.x
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    assert isinstance(self.app.plan[1][B].place, Place),self.app.plan[1][B].place
    assert isinstance(self.app.plan[1][B].thing.place, Way),self.app.plan[1][B].thing.place

  def _check_after_take(self,A,B,P=Place, T= Trunk):
    assert isinstance(self.app.plan[1][A], Way),self.app.plan[1][A]
    assert isinstance(self.app.plan[1][A].place, Place),self.app.plan[1][A].place
    assert isinstance(self.app.plan[1][A].thing, P),self.app.plan[1][A].thing
    assert isinstance(self.app.plan[1][B].thing.place, Door),self.app.plan[1][B].thing.place
    assert self.app.plan[1][B].thing.thing.x==B,self.app.plan[1][B].thing.thing.x
    assert self.app.plan[1][B].thing.x==B,self.app.plan[1][B].thing.x
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    assert isinstance(self.app.plan[1][B].place, Place),self.app.plan[1][B].place
    assert isinstance(self.app.plan[1][B].thing.place, Door),self.app.plan[1][B].thing.place
    assert isinstance(self.app.plan[1][B].thing.thing, T),self.app.plan[1][B].thing.thing

  def _check_after_move(self,A,B,C=Way,D=Door, P= Place, T=Place):
    assert self.app.actor.x == A,self.app.actor.x
    #assert self.app.actor.thing == self.app.plan[1][A].place,self.app.actor.thing
    assert self.app.actor.place == self.app.plan[1][A],self.app.actor.place
    assert isinstance(self.app.plan[1][B], D),self.app.plan[1][B]
    assert isinstance(self.app.plan[1][B].thing, P),self.app.plan[1][B].thing
    assert isinstance(self.app.plan[1][B].place, Place),self.app.plan[1][B].place
    assert isinstance(self.app.plan[1][A], C),self.app.plan[1][A]
    assert self.app.plan[1][A].thing == self.app.actor,self.app.plan[1][A].thing 
    assert isinstance(self.app.plan[1][A].thing, Actor),self.app.plan[1][A].thing
    assert isinstance(self.app.plan[1][A].thing.thing, T),self.app.plan[1][A].thing.thing
  def _replay_and_create_place(self,p = '.&.'):
    "create place"
    self.mock_gui.replay()
    self.app = main(self.mg, self.mg, self.mg, p)
    print('---- NOW OPERATIONS ----')
  def testa_cria_place(self):
    "create place"
    self._expect_all_place()
    self._replay_and_create_place()
  def testa_move_forward(self):
    "move forward"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place()
    B, A = 2,3
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    self.app.actor.go_forward()
    self._check_after_move(A,B,C=Way,D=Door)
  def testa_cant_move_forward(self):
    "cant move forward"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place('.&')
    B, A = 2,2
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    self.app.actor.go_forward()
    self._check_after_move(A,B,C=Door,D=Door, P=Actor)
  def testa_move_forward_and_back(self):
    "move forward and back"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place()
    B, A = 3,2
    print('NOW MOVING FORE')
    self.app.actor.go_forward()
    assert isinstance(self.app.plan[1][A].thing, Place),self.app.plan[1][A].thing
    self._check_after_move(B,A,C=Way,D=Door)
    print('NOW MOVING BACK')
    self.app.actor.go_backward()
    self._check_after_move(A,B,D=Way,C=Door)
  def testa_take_forward(self):
    "take forward"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place('.&$.')
    B, A = 2,3
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    self.app.actor.go_take()
    self._check_after_take(A,B)
    assert isinstance(self.app.plan[1][B].thing.thing.place, Actor),self.app.plan[1][B].place
  def testa_take_nothing(self):
    "take nothing"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place('.&..')
    B, A = 2,3
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    self.app.actor.go_take()
    self._check_after_take(A,B,T=Place)
    #assert isinstance(self.app.plan[1][B].thing.thing.place, Actor),self.app.plan[1][B].place
  def testa_give_nothing(self):
    "give nothing"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place('.&..')
    B, A = 2,3
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    self.app.actor.go_give()
    self._check_after_take(A,B,P=Place,T=Place)
    #assert isinstance(self.app.plan[1][B].thing.thing.place, Actor),self.app.plan[1][B].place
  def testa_give_forward(self):
    "give forward"
    self._expect_all_place()
    expect(self.ma.get_direction()).count(1,2).result(1)
    expect(self.ma.move(ARGS)).count(1,2)
    self._replay_and_create_place('.&$.')
    B, A = 2,3
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    self.app.actor.go_take()
    self._check_after_take(A,B)
    assert isinstance(self.app.plan[1][B].thing.thing.place, Actor),self.app.plan[1][B].place
    print('NOW GIVING BACK')
    self.app.actor.go_give()
    self._check_after_take(A,B,P=Trunk, T=Place)
    assert self.app.plan[1][A].thing.x == A,self.app.plan[1][A].thing.x
    
  def testa_move_with_taken(self):
    "take and move"
    self._expect_all_place()
    expect(self.ma.get_direction()).count(1,2).result(1)
    expect(self.ma.move(ARGS)).count(1,2)
    self._replay_and_create_place('.&$.')
    B, A = 2,3
    assert isinstance(self.app.plan[1][B].thing, Actor),self.app.plan[1][B].thing
    self.app.actor.go_take()
    self._check_after_take(A,B)
    assert isinstance(self.app.plan[1][B].thing.thing.place, Actor),self.app.plan[1][B].place
    B, A = 3,2
    print('NOW MOVING FORE')
    self.app.actor.go_forward()
    assert isinstance(self.app.plan[1][A].thing, Place),self.app.plan[1][A].thing
    self._check_after_move(B,A,C=Way,D=Door, T=Trunk)
    assert self.app.actor.thing.x == A,self.app.actor.thing.x
    assert isinstance(self.app.actor.thing, Trunk),self.app.actor.thing
  def testa_push_forward(self):
    "push forward"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place()
    B, A = 2,3
    self.app.actor.go_push()
    assert isinstance(self.app.plan[1][B].thing, Place),self.app.plan[1][B].thing
    self._check_after_move(A,B)

  def testa_push_trunk(self):
    "push trunk"
    self._expect_all_place()
    expect(self.ma.get_direction()).count(1,6).result(1)
    expect(self.ma.move(ARGS)).count(1,2)
    self._replay_and_create_place('.&$.')
    B, A, P = 2,3, 4
    assert isinstance(self.app.plan[1][B].thing.place, Door),self.app.plan[1][B].thing.place
    self.app.actor.go_push()
    self._check_after_move(A,B)
    B, A, P = 3, 4, 5
    self._check_after_push(A,B)
  def ntesta_push_trunk_twice(self):
    "push trunk twice"
    self._expect_all_place()
    expect(self.ma.get_direction()).count(1,6).result(1)
    expect(self.ma.move(ARGS)).count(1,3)
    self._replay_and_create_place('.&$..')
    B, A, P = 2, 3, 4
    print('NOW PUSHING FORE')
    self.app.actor.go_push()
    self._check_after_move(A,B)
    #assert isinstance(self.app.plan[1][P].thing, Trunk),self.app.plan[1][P].thing
    B, A, P = 3, 4, 5
    self._check_after_push(A,B)
    print('NOW PUSHING FORE AGAIN')
    self.app.actor.go_push()
    self._check_after_move(A,B, D=Way)
    B, A, P = 4, 5, 6
    self._check_after_push(A,B)
    assert isinstance(self.app.plan[1][P].thing, Trunk),self.app.plan[1][P].thing
    #assert False

if __name__ == '__main__':
    import unittest
    unittest.main()
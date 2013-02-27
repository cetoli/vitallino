"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/01/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.2 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: 2011, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.2 $Revision$"[10:-1]
__date__    = "2013/02/09 $Date$"
"""
if '__package__' in dir():
    from parts import Cell
    pass
    
def inherit(base, child):
    overriden, inherited = dir(child), dir(base)
    for member in inherited:
        if member not in overriden:
            setattr(child, member, getattr(base,member))
    #child.m =  str(child.__class__)
    return base

class Way:
    def __init__(self, avatar, place, x, y, me=None, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        self.avatar,self.place = avatar, place
        self.thing, self.x, self.y, self.m = place, x, y, self

class Tar:
    def leave(self,thing, action, reverse =0):
        print('Youre STUCK!!!')
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)

class Door:
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        place.x, place.y =  x, y

class Entry:
    def __init__(self, thing, entry, x, y):
        self.x, self.y, self.entry, self.thing = x, y, entry, thing
    def get_entry(self):
        return self.thing
    def get_direction(self):
        return self.entry.get_direction()
    def get_position(self):
        return (self.x, self.y)

class Trunk:
    def clear(self, load= None):
        print( '%s.clear, position %d %d thing %s load %s'%(
            self.m, self.x, self.y, self.thing, load ))
        self.thing = load or PLACE#self.place
    def reset(self):
        self.move_entry = self.null_move_entry
        self.entry.reset()
    def get_direction(self):
        return self.avatar.get_direction()
    def get_position(self,x=0, y=0):
        return (self.x, self.y)
    def enter(self,entry, destination ):
        print('It is HEAVY!!')
        entry.reset()
    def take(self,entry,direction ):
        print('Hands Busy!!')
        entry.reset()
    def _move(self, loc):
        self.place.clear()
        self.x, self.y = loc.x, loc.y
        self.place = loc
        loc.clear(self)
        ##print( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.thing.get_real_position(x=loc.x, y=loc.y)
        print( '%s(trunk).move, position %d %d  entry%s real %d %d'%(
            self.m,loc.x, loc.y, loc, mx, my))
        avatar.move(mx, my)
    def move_entry(self,loc):
        pass
    def null_move_entry(self,loc):
        pass
    def move(self, loc):
        place = self.place
        self._move(loc)
        self.move_entry(place)
    def given(self,entry, destination):
        self._move(destination)
        #self.thing.give(self, destination)
    def give(self, entry, direction):
        self.thing.give(self, direction)
    def taken(self,entry, destination):
        entry.take(self)
    def pushed(self,entry, destination ):
        def _move_entry(loc, entry= entry, self= self):
            entry.move(loc)
            self.move_entry = self.null_move_entry
        self.move_entry = _move_entry
        self.heading = entry.heading
        self.entry = entry
        print( '%s(trunk).pushed,thing %s entry %s destination %s direction %s'%(
            self.m, self.thing, entry, destination, entry.heading))
        self.thing.push(self, entry.heading)
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        self.avatar,self.place = avatar, place
        self.thing, self.x, self.y, self.m = place, x, y, self
    def rebase(self,base):
        place = Way(None,self, self.x, self.y)
        base[self.y][self.x]= place
        place.place = self.place
        place.thing = self
        self.place = place

class Rock:
    def clear(self, load= None):
        print( '%s.clear, position %d %d thing %s load %s'%(
            self.m, self.x, self.y, self.thing, load ))
        self.thing = load or PLACE#self.place
    def reset(self):
        self.move_entry = self.null_move_entry
        self.entry.reset()
    def get_direction(self):
        return self.avatar.get_direction()
    def get_position(self,x=0, y=0):
        return (self.x, self.y)
    def _move(self, loc):
        self.place.clear()
        self.x, self.y = loc.x, loc.y
        self.place = loc
        loc.clear(self)
        ##print( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.thing.get_real_position(x=loc.x, y=loc.y)
        print( '%s(rock).move, position %d %d  entry%s real %d %d'%(
            self.m,loc.x, loc.y, loc, mx, my))
        avatar.move(mx, my)
    def move_entry(self,loc):
        pass
    def null_move_entry(self,loc):
        pass
    def move(self, loc):
        place = self.place
        self._move(loc)
        self.move_entry(place)
    def taken(self,entry, destination):
        print('Too much Heavy to take!!')
        entry.reset()
    def enter(self,entry, destination ):
        print('It is HEAVY!!')
        entry.reset()
    def pushed(self,entry, destination ):
        def _move_entry(loc, entry= entry, self= self):
            entry.move(loc)
            self.move_entry = self.null_move_entry
        self.move_entry = _move_entry
        self.heading = entry.heading
        self.entry = entry
        print( '%s(rock).pushed,thing %s entry %s destination %s direction %s'%(
            self.m, self.thing, entry, destination, entry.heading))
        self.thing.push(self, entry.heading)
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        self.avatar,self.place = avatar, place
        self.thing, self.x, self.y, self.m = place, x, y, self
    def rebase(self,base):
        place = Way(None,self, self.x, self.y)
        base[self.y][self.x]= place
        place.place = self.place
        place.thing = self
        self.place = place

class Border:
    def enter(self,entry, destination ):
        print('Cant go this way!!')
        entry.reset()
    def pushed(self,entry, destination ):
        print('Cant go this way!!')
        entry.reset()
    def given(self,entry, destination ):
        print('Cant give this way!!')
        entry.reset()
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        self.thing, self.x, self.y, self.m = place, x, y, self
        self.place = place #Way(None,place, self.x, self.y)
        #self.avatar,self.place, self.x, self.y = avatar, place, x, y


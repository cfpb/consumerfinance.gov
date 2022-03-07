import {
  assign,
  toArray
} from '../../../../../../../cfgov/unprocessed/js/routes/on-demand/youth-employment-programs/buying-a-car/util.js';

describe('YEP utility functions', () => {
  describe('assign', () => {
    const originalObject = {
      agency: 'CFPB'
    };

    it('merges a single object', () => {
      const sourceObj = { team: 'D and D' };
      const nextObj = assign(originalObject, sourceObj);

      expect(nextObj.agency).toBe(originalObject.agency);
      expect(nextObj.team).toBe(sourceObj.team);
    });

    it('merges multiple objects', () => {
      const team = { team: 'engineering' };
      const guild = { guild: 'front-end' };
      const merged = assign(originalObject, team, guild);

      expect(merged.team).toBe(team.team);
      expect(merged.guild).toBe(guild.guild);
      expect(merged.agency).toBe(originalObject.agency);
    });

    it('overwrites properties of the original object', () => {
      const override = { agency: 'GSA' };
      expect(assign(originalObject, override).agency)
        .toBe(override.agency);
    });

    it('does not mutate the original object', () => {
      expect(assign(originalObject)).not.toBe(originalObject);
    });
  });

  describe('.toArray', () => {
    it('turns array-like values into arrays', () => {
      const number = toArray(1);
      expect(number.length).toBe(0);

      const string = toArray('ab');
      expect(string.length).toBe(2);
      expect(string[0]).toBe('a');

      const obj = toArray({});
      expect(obj.length).toBe(0);

      const fragment = document.createDocumentFragment();
      const children = [
        document.createElement('a'),
        document.createElement('a')
      ];
      children.forEach(child => fragment.appendChild(child));

      const dom = document.createElement('div');
      dom.appendChild(fragment);
      const array = toArray(dom.querySelectorAll('a'));

      expect(array.slice).toBeDefined();
    });
  });
});

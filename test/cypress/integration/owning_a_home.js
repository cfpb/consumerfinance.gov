import { ExploreRates, Feedback } from '../pages/owning_a_home';

let exploreRates = new ExploreRates();
let feedback = new Feedback();
describe('Owning a Home', () => {
  
  describe('Explore Rates', () => {
    it('Should load the interest rates graph when a state has changed', () => {
      exploreRates.open();
      exploreRates.selectState('Virginia');
      exploreRates.graph().should('exist')
    });
  });

  describe('Feedback', () => {
    it('Should submit feedback', () => {
      feedback.open();
      feedback.submitComment("This is a test comment");
      feedback.successNotification().should('be.visible')
    });
  });
    
});

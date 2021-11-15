# Xed - Re-imagining Travelling during the Covid-19 Pandemic

## Inspiration
A few months back, one of our teammates wanted to visit family in Australia. Unfortunately for them, the process of finding cheap flights, booking them, and finding current government-recommended Covid-19 guidelines was extremely stressful and nerve-wracking. A lot of time was spent on researching whether their vaccination status was recognized by the Australian government, and how long they'd need to quarantine for, among other things. According to us, such a problem should have never been a problem in the first place. We'd like to change that. This is why we've built *Xed*, a unique platform that helps remove the stress in travelling so you can worry about the things that *really matter*.

## What it does
*Xed* is a web platform, run entirely on Redhat's OpenShift, that shows travellers all the necessary information they'd require when making an international trip. We allow users to enter cities they'd like to travel to, and *Xed* displays *cheap flights*, *nearby hotels from the airport*, *recommended tourist spots* as well as *local Covid-19 guidelines for their destination city* such as the overall Covid-19 risk, quarantine requirements, as well as government-issued recommendations for safe travel. 

*Xed* provides answers to the following questions that travellers may have:
1. Can I travel to this particular city? Are the borders closed for international travellers?
2. Is it safe to travel to my destination? How much of a Covid-19 risk exists there? Am I potentially travelling into a Covid-19 hotspot?
3. What are the quarantine requirements at my destination? How long would I have to quarantine for? Are there any hotels (or similar resting places) that I can book cheap stays at during this period?
4. What are the Covid-19 testing procedures at my destination? Do I have to issue a Covid-19-negative certificate at the airport?
5. Is my vaccination status counted? If not, what are the recognized vaccines by my destination's government?

## How we built it
We build *Xed* entirely in Python with Flask running on the backend. We added HTML/CSS and JavaScript code to add a bit of functionality to the website. To actually get real-time flight data and Covid-19 travel restrictions data, we relied on an external API service, [Amadeus](http://amadeus.com). Finally, the entire application was powered by RedHat's OpenShift's production servers.

## Challenges we ran into
We entered this hackathon pretty late. This meant that we had to come up with an idea, build on our solution, and present it all in the span of 4 days! We had a few people on our team quit midway, and it was left on us, complete DevOps-beginners, to build the remaining portion of our project. We also had to work with the restrictions that the testing sandbox environment of Amadeus' APIs imposed on us.

## Accomplishments that we're proud of
We're proud of what we've built in such a short amount of time. We've learned so much about working with APIs, processing data in real-time, and sending the results back to the server. This was also our first time using the OpenShift platform, and since we are all complete beginners to DevOps, we were grateful for OpenShift's incredibly low learning curve.

## What's next for Xed
Xed, admittedly, is not complete. There are a few bugs in the code -- most notably because of us running Amadeus' API on a testing sandbox environment (the production version was a paid option) -- that we'd like to tackle. We plan on working on this idea further, and possibly taking *Xed* to a much larger platform. For this, we'd first improve existing features, as well as add a feature to add hotel/flight booking functionality which would allow the user to book a hotel/flight directly from *Xed*. A future goal of ours, though not immediate, is to be able to process the real-time data faster, thus improving the overall user experience. For this, we have begun exploring more robust options such as Apache Kafka. 

## Important Notes:
If the link to our project on Openshift appears to be down, please contact us to restart our pods (since they're only active for about 12 hours). We will do our best to respond as quickly as we can. 

Additionally, we'd like to stress that with the limited amount of time that we had, as well as severe restrictions running a sandbox environment API, we've noticed that entering a few cities crashes the server on Openshift. But don't worry -- trying to submit the form a second time usually works. This is on the top of our minds as something we'd like to fix (including purchasing the production version of the Amadeus API) when we get the chance to scale *Xed* onto a much larger platform.